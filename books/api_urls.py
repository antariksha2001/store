from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    BookViewSet, 
    CategoryViewSet, 
    cart_api, 
    update_cart_item,
    featured_books,
    book_detail_api
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')

# Wire up our API using automatic URL routing
urlpatterns = [
    path('', include(router.urls)),
    path('cart/', cart_api, name='cart-api'),
    path('cart/update/<int:book_id>/', update_cart_item, name='update-cart-item'),
    path('featured/', featured_books, name='featured-books-api'),
    path('book/<slug:slug>/', book_detail_api, name='book-detail-api'),
]
