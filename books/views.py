from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book, Category
from decimal import Decimal


def home(request):
    """Homepage with featured books"""
    featured_books = Book.objects.filter(is_available=True).order_by('-created_at')[:12]
    categories = Category.objects.all()
    
    context = {
        'featured_books': featured_books,
        'categories': categories,
    }
    return render(request, 'books/home.html', context)


def book_detail(request, slug):
    """Book details page"""
    book = get_object_or_404(Book, slug=slug, is_available=True)
    related_books = Book.objects.filter(
        category=book.category, 
        is_available=True
    ).exclude(id=book.id)[:4]
    
    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'books/book_detail.html', context)


def book_list(request):
    """List all books with filtering"""
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()
    
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_slug:
        books = books.filter(category__slug=category_slug)
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query or '',
    }
    return render(request, 'books/book_list.html', context)


@require_POST
def add_to_cart(request):
    """Add book to cart"""
    book_id = str(request.POST.get('book_id'))
    quantity = int(request.POST.get('quantity', 1))
    
    book = get_object_or_404(Book, id=book_id, is_available=True)
    
    cart = request.session.get('cart', {})
    
    if book_id in cart:
        cart[book_id]['quantity'] += quantity
    else:
        cart[book_id] = {
            'title': book.title,
            'author': book.author,
            'price': str(book.price),
            'quantity': quantity,
            'image': book.image.url if book.image else None,
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f'"{book.title}" added to cart!')
    
    return redirect('books:book_detail', slug=book.slug)


@require_POST
def update_cart(request):
    """Update cart item quantity"""
    book_id = str(request.POST.get('book_id'))
    quantity = int(request.POST.get('quantity', 1))
    
    cart = request.session.get('cart', {})
    
    if book_id in cart:
        if quantity > 0:
            cart[book_id]['quantity'] = quantity
        else:
            del cart[book_id]
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('books:cart_view')


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    book_id = str(request.POST.get('book_id'))
    
    cart = request.session.get('cart', {})
    
    if book_id in cart:
        del cart[book_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, 'Item removed from cart!')
    
    return redirect('books:cart_view')


def cart_view(request):
    """Shopping cart page"""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal('0.00')
    
    for book_id, item in cart.items():
        quantity = int(item['quantity'])
        price = Decimal(item['price'])
        item_total = price * quantity
        total_price += item_total
        
        cart_item = {
            'book_id': book_id,
            'title': item['title'],
            'author': item['author'],
            'price': price,
            'quantity': quantity,
            'image': item['image'],
            'item_total': item_total,
        }
        cart_items.append(cart_item)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(int(item['quantity']) for item in cart.values()),
    }
    
    return render(request, 'books/cart.html', context)


def search_books(request):
    """Search books"""
    query = request.GET.get('q', '')
    books = Book.objects.filter(is_available=True)
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    context = {
        'books': books,
        'query': query,
    }
    
    return render(request, 'books/search_results.html', context)


def about_page(request):
    """About Us page"""
    context = {
        'title': 'About Us',
        'description': 'Learn about our bookstore and our mission to provide quality books to readers.',
    }
    return render(request, 'books/about.html', context)


def contact_page(request):
    """Contact Us page"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Save contact message to database
        from .models import ContactMessage
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Here you would typically send an email notification
        # send_email_notification(name, email, subject, message)
        
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('books:contact_page')
    
    context = {
        'title': 'Contact Us',
        'description': 'Get in touch with us for any questions or feedback.',
    }
    return render(request, 'books/contact.html', context)
