from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Customer, Order, OrderItem
from books.models import Book
from .forms import CheckoutForm
from decimal import Decimal


def checkout(request):
    """Checkout page"""
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('books:cart_view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create customer
                customer = Customer.objects.create(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                )
                
                # Calculate total price
                total_price = Decimal('0.00')
                for book_id, item in cart.items():
                    total_price += Decimal(item['price']) * item['quantity']
                
                # Create order
                order = Order.objects.create(
                    customer=customer,
                    total_price=total_price,
                    status='pending'
                )
                
                # Create order items and update book availability
                for book_id, item in cart.items():
                    book = Book.objects.get(id=book_id)
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=item['quantity'],
                        price=Decimal(item['price'])
                    )
                    
                    # Mark book as sold
                    book.is_available = False
                    book.save()
                
                # Clear cart
                request.session['cart'] = {}
                
                messages.success(request, f'Order #{order.id} placed successfully!')
                return redirect('orders:order_success', order_id=order.id)
    else:
        form = CheckoutForm()
    
    # Calculate cart total for display
    cart_items = []
    total_price = Decimal('0.00')
    
    for book_id, item in cart.items():
        item_total = Decimal(item['price']) * item['quantity']
        total_price += item_total
        
        cart_items.append({
            'book_id': book_id,
            'title': item['title'],
            'author': item['author'],
            'price': Decimal(item['price']),
            'quantity': item['quantity'],
            'image': item['image'],
            'item_total': item_total,
        })
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_success.html', context)


def order_history(request):
    """Order history (for future customer account feature)"""
    # This would be implemented with customer authentication
    orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_history.html', context)
