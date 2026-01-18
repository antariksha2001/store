from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Book, Category
from .serializers import BookSerializer, BookListSerializer, CategorySerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_books(request):
    """API endpoint to get featured/available books"""
    books = Book.objects.filter(is_available=True).order_by('-created_at')[:12]
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail_api(request, book_id):
    """API endpoint to get book details"""
    try:
        book = Book.objects.get(id=book_id, is_available=True)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found or not available'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def add_to_cart_api(request):
    """API endpoint to add book to cart"""
    book_id = request.data.get('book_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        book = Book.objects.get(id=book_id, is_available=True)
        
        cart = request.session.get('cart', {})
        
        if str(book_id) in cart:
            cart[str(book_id)]['quantity'] += int(quantity)
        else:
            cart[str(book_id)] = {
                'title': book.title,
                'author': book.author,
                'price': str(book.price),
                'quantity': int(quantity),
                'image': book.image.url if book.image else None,
            }
        
        request.session['cart'] = cart
        
        return Response({
            'success': True,
            'message': f'"{book.title}" added to cart!',
            'cart_count': sum(item['quantity'] for item in cart.values())
        })
        
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found or not available'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def remove_from_cart_api(request):
    """API endpoint to remove book from cart"""
    book_id = request.data.get('book_id')
    
    cart = request.session.get('cart', {})
    
    if str(book_id) in cart:
        del cart[str(book_id)]
        request.session['cart'] = cart
        
        return Response({
            'success': True,
            'message': 'Item removed from cart!',
            'cart_count': sum(item['quantity'] for item in cart.values())
        })
    else:
        return Response(
            {'error': 'Item not found in cart'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def cart_api(request):
    """API endpoint to get cart contents"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for book_id, item in cart.items():
        item_total = float(item['price']) * item['quantity']
        total_price += item_total
        
        cart_items.append({
            'book_id': book_id,
            'title': item['title'],
            'author': item['author'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'image': item['image'],
            'item_total': item_total,
        })
    
    return Response({
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(item['quantity'] for item in cart.values())
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def search_books_api(request):
    """API endpoint to search books"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    
    books = Book.objects.filter(is_available=True)
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category:
        books = books.filter(category__slug=category)
    
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def categories_api(request):
    """API endpoint to get all categories"""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)
