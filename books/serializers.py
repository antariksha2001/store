from rest_framework import serializers
from .models import Book, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'description', 
            'price', 'image', 'is_available', 'category', 
            'created_at', 'updated_at'
        ]


class BookListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'price', 
            'image', 'category_name', 'created_at'
        ]
