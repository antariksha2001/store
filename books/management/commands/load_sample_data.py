import os
import django
from django.core.management.base import BaseCommand
from django.conf import settings
from books.models import Book, Category
from django.utils.text import slugify
from books.models import Book, Category
import random


class Command(BaseCommand):
    help = 'Load sample books and categories into the database'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            'Fiction', 'Non-Fiction', 'Science Fiction', 'Mystery', 'Romance',
            'Biography', 'History', 'Self-Help', 'Technology', 'Business',
            'Children', 'Young Adult', 'Poetry', 'Cooking', 'Travel'
        ]

        categories = {}
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name)}
            )
            categories[cat_name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Sample books data with INR prices
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'description': 'A classic American novel set in the Jazz Age, exploring themes of wealth, love, and the American Dream through the mysterious Jay Gatsby.',
                'price': 299.00,
                'category': 'Fiction'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'description': 'A powerful story of racial injustice and childhood innocence in the American South during the 1930s.',
                'price': 399.00,
                'category': 'Fiction'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'A dystopian social science fiction novel that follows the life of Winston Smith under totalitarian rule.',
                'price': 349.00,
                'category': 'Science Fiction'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'description': 'A romantic novel of manners that charts the emotional development of the protagonist Elizabeth Bennet.',
                'price': 299.00,
                'category': 'Romance'
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'description': 'The story of teenage rebellion and angst, narrated by the iconic Holden Caulfield.',
                'price': 349.00,
                'category': 'Fiction'
            },
            {
                'title': 'Harry Potter and the Sorcerer\'s Stone',
                'author': 'J.K. Rowling',
                'description': 'The first book in the beloved series about a young wizard\'s magical education and adventures.',
                'price': 599.00,
                'category': 'Children'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'description': 'A fantasy adventure about Bilbo Baggins\' unexpected journey with dwarves to reclaim their mountain home.',
                'price': 499.00,
                'category': 'Fiction'
            },
            {
                'title': 'Sapiens: A Brief History of Humankind',
                'author': 'Yuval Noah Harari',
                'description': 'An exploration of how Homo sapiens came to dominate the world, examining biology, anthropology, and history.',
                'price': 799.00,
                'category': 'Non-Fiction'
            },
            {
                'title': 'Educated',
                'author': 'Tara Westover',
                'description': 'A memoir about a woman who grows up in a survivalist family and goes on to earn a PhD from Cambridge University.',
                'price': 699.00,
                'category': 'Biography'
            },
            {
                'title': 'The Girl with the Dragon Tattoo',
                'author': 'Stieg Larsson',
                'description': 'A gripping thriller combining murder mystery, family saga, love story, and financial intrigue.',
                'price': 449.00,
                'category': 'Mystery'
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'description': 'A philosophical story about Santiago, an Andalusian shepherd boy who dreams of finding treasure in Egypt.',
                'price': 299.00,
                'category': 'Fiction'
            },
            {
                'title': 'Thinking, Fast and Slow',
                'author': 'Daniel Kahneman',
                'description': 'A groundbreaking tour of the mind that explains the two systems that drive the way we think and make decisions.',
                'price': 899.00,
                'category': 'Non-Fiction'
            },
            {
                'title': 'The Hunger Games',
                'author': 'Suzanne Collins',
                'description': 'A dystopian novel set in Panem, where the Capitol forces young tributes to fight to the death on live television.',
                'price': 449.00,
                'category': 'Young Adult'
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'description': 'A mystery thriller that follows symbologist Robert Langdon as he investigates a murder in the Louvre Museum.',
                'price': 499.00,
                'category': 'Mystery'
            },
            {
                'title': 'Atomic Habits',
                'author': 'James Clear',
                'description': 'A practical guide to building good habits and breaking bad ones, with proven strategies for lasting change.',
                'price': 599.00,
                'category': 'Self-Help'
            },
            {
                'title': 'The Midnight Library',
                'author': 'Matt Haig',
                'description': 'A novel about a magical library between life and death where you can try out different versions of your life.',
                'price': 449.00,
                'category': 'Fiction'
            },
            {
                'title': 'Where the Crawdads Sing',
                'author': 'Delia Owens',
                'description': 'A coming-of-age murder mystery set in the marshes of North Carolina, following the life of Kya Clark.',
                'price': 549.00,
                'category': 'Mystery'
            },
            {
                'title': 'The Lean Startup',
                'author': 'Eric Ries',
                'description': 'A guide for how today\'s entrepreneurs can use continuous innovation to create radically successful businesses.',
                'price': 699.00,
                'category': 'Business'
            },
            {
                'title': 'Steve Jobs',
                'author': 'Walter Isaacson',
                'description': 'The authorized biography of Apple\'s co-founder, based on extensive interviews with Jobs and those who knew him.',
                'price': 999.00,
                'category': 'Biography'
            },
            {
                'title': 'The Silent Patient',
                'author': 'Alex Michaelides',
                'description': 'A psychological thriller about a woman who allegedly kills her husband and then never speaks another word.',
                'price': 399.00,
                'category': 'Mystery'
            }
        ]

        # Create books with images
        created_count = 0
        for i, book_data in enumerate(books_data):
            category = categories.get(book_data['category'])
            if category:
                # Download book cover image
                image_url = f"https://picsum.photos/seed/book-{i+1}/300/400"
                image_filename = f"book_{i+1}.jpg"
                image_path = os.path.join(settings.MEDIA_ROOT, 'book_covers', image_filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                
                # Download image
                try:
                    import urllib.request
                    urllib.request.urlretrieve(image_url, image_path)
                    image_relative_path = f'book_covers/{image_filename}'
                except:
                    image_relative_path = None
                
                book, created = Book.objects.get_or_create(
                    title=book_data['title'],
                    defaults={
                        'slug': slugify(book_data['title']),
                        'author': book_data['author'],
                        'description': book_data['description'],
                        'price': book_data['price'],
                        'category': category,
                        'is_available': True,
                        'image': image_relative_path
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Created book: {book.title} with image'))

        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created_count} sample books')
        )
