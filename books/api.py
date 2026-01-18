from rest_framework import serializers
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book, Category
from decimal import Decimal


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author', 'description', 'price', 'price_display', 
                  'image', 'is_available', 'category', 'category_name', 'created_at']
    
    def get_price_display(self, obj):
        return f"₹{obj.price:.2f}"


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'book_count', 'created_at']
    
    def get_book_count(self, obj):
        return obj.book_set.filter(is_available=True).count()


class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    title = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_items = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price_display = serializers.SerializerMethodField()
    
    def get_total_price_display(self, obj):
        return f"₹{obj['total_price']:.2f}"


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view all books
    """
    queryset = Book.objects.filter(is_available=True)
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_available=True)
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        
        if category:
            queryset = queryset.filter(category__slug=category)
        
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                author__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        # Featured books (top 8 by price)
        featured = self.request.query_params.get('featured')
        if featured:
            queryset = queryset.order_by('-price')[:8]
        
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint to view all categories
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([AllowAny])
def cart_api(request):
    """
    API endpoint to handle shopping cart operations
    """
    if request.method == 'GET':
        # Get cart from session
        cart = request.session.get('cart', {})
        
        # Calculate cart details
        items = []
        total_price = Decimal('0.00')
        total_items = 0
        
        for book_id, item_data in cart.items():
            try:
                book = Book.objects.get(id=int(book_id), is_available=True)
                quantity = item_data.get('quantity', 1)
                item_total = book.price * quantity
                
                items.append({
                    'book_id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'price': float(book.price),
                    'quantity': quantity,
                    'total': float(item_total),
                    'image': book.image.url if book.image else None
                })
                
                total_price += item_total
                total_items += quantity
                
            except Book.DoesNotExist:
                continue
        
        cart_data = {
            'items': items,
            'total_items': total_items,
            'total_price': float(total_price)
        }
        
        serializer = CartSerializer(cart_data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Add item to cart
        book_id = str(request.data.get('book_id'))
        quantity = request.data.get('quantity', 1)
        
        if not book_id:
            return Response(
                {'error': 'Book ID is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            book = Book.objects.get(id=int(book_id), is_available=True)
            
            # Get or create cart
            cart = request.session.get('cart', {})
            
            # Add or update item in cart
            if book_id in cart:
                cart[book_id]['quantity'] += quantity
            else:
                cart[book_id] = {
                    'quantity': quantity
                }
            
            # Save cart to session
            request.session['cart'] = cart
            request.session.modified = True
            
            return Response({
                'message': 'Item added to cart successfully',
                'cart_total': sum(item['quantity'] for item in cart.values())
            })
            
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    elif request.method == 'DELETE':
        # Clear cart or remove specific item
        book_id = request.data.get('book_id')
        cart = request.session.get('cart', {})
        
        if book_id:
            # Remove specific item
            if book_id in cart:
                del cart[book_id]
                request.session['cart'] = cart
                request.session.modified = True
                
                return Response({
                    'message': 'Item removed from cart',
                    'cart_total': sum(item['quantity'] for item in cart.values())
                })
            else:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Clear entire cart
            request.session['cart'] = {}
            request.session.modified = True
            
            return Response({
                'message': 'Cart cleared successfully'
            })


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_cart_item(request, book_id):
    """
    API endpoint to update cart item quantity
    """
    try:
        book = Book.objects.get(id=int(book_id), is_available=True)
        quantity = request.data.get('quantity', 1)
        
        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than 0'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart = request.session.get('cart', {})
        
        if str(book_id) in cart:
            cart[str(book_id)]['quantity'] = quantity
            request.session['cart'] = cart
            request.session.modified = True
            
            return Response({
                'message': 'Cart item updated successfully',
                'quantity': quantity
            })
        else:
            return Response(
                {'error': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_books(request):
    """
    API endpoint to get featured books
    """
    featured_books = Book.objects.filter(is_available=True).order_by('-price')[:8]
    serializer = BookSerializer(featured_books, many=True)
    
    return Response({
        'featured_books': serializer.data,
        'count': len(serializer.data)
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail_api(request, slug):
    """
    API endpoint to get book details by slug
    """
    book = get_object_or_404(Book, slug=slug, is_available=True)
    serializer = BookSerializer(book)
    
    return Response(serializer.data)
