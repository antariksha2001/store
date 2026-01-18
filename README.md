# Online Bookstore - Django Web Application

A complete and advanced Online Bookstore Web Application built with Django Framework, featuring a modern UI/UX design, shopping cart functionality, and RESTful APIs.

## Features

### 🏠 **Homepage**
- Dynamic featured books display
- Professional hero section
- Category browsing
- Search functionality
- Responsive design

### 📚 **Book Management**
- Detailed book pages
- Book categorization
- Availability tracking
- Image support
- Search and filtering

### 🛒 **Shopping Cart**
- Session-based cart system
- Add/remove items
- Quantity management
- Real-time price calculation
- Cart persistence

### 💳 **Checkout System**
- Secure checkout form
- Customer information collection
- Order processing
- Automatic book availability updates
- Order confirmation

### 🔧 **Admin Panel**
- Book management
- Category management
- Order tracking
- Customer data

### 🌐 **REST API**
- Django REST Framework integration
- Book listing endpoints
- Cart management APIs
- Search functionality
- Category endpoints

### 🎨 **Modern UI/UX**
- Bootstrap 5 styling
- Responsive design
- Smooth animations
- Professional layout
- Mobile-friendly

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MySQL/PostgreSQL
- **Frontend**: Bootstrap 5, Font Awesome
- **API**: Django REST Framework
- **Images**: Pillow for image handling
- **Configuration**: python-decouple

## Installation

### Prerequisites
- Python 3.8+
- MySQL or PostgreSQL
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd djangobooks
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env` file and update with your database credentials:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   DB_NAME=bookstore
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

5. **Create database**
   ```sql
   CREATE DATABASE bookstore CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

9. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

10. **Run development server**
    ```bash
    python manage.py runserver
    ```

11. **Access the application**
    - Website: http://127.0.0.1:8000/
    - Admin Panel: http://127.0.0.1:8000/admin/
    - API Documentation: http://127.0.0.1:8000/api/

## API Endpoints

### Books
- `GET /api/books/featured/` - Get featured books
- `GET /api/books/<id>/` - Get book details
- `GET /api/books/search/` - Search books

### Cart
- `GET /api/cart/` - Get cart contents
- `POST /api/cart/add/` - Add item to cart
- `POST /api/cart/remove/` - Remove item from cart

### Categories
- `GET /api/categories/` - Get all categories

## Project Structure

```
djangobooks/
├── bookstore/           # Django project settings
├── books/              # Books app
│   ├── models.py       # Book and Category models
│   ├── views.py        # Book views
│   ├── urls.py         # Book URLs
│   ├── api_views.py    # API views
│   ├── serializers.py  # API serializers
│   └── management/     # Management commands
├── orders/             # Orders app
│   ├── models.py       # Order models
│   ├── views.py        # Order views
│   ├── forms.py        # Checkout form
│   └── urls.py         # Order URLs
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── media/             # Uploaded files
└── manage.py          # Django management script
```

## Database Models

### Books App
- **Category**: Book categories (Fiction, Non-Fiction, etc.)
- **Book**: Book information with availability tracking

### Orders App
- **Customer**: Customer information
- **Order**: Order details and status
- **OrderItem**: Individual items in an order

## Features Implementation

### Shopping Cart
- Session-based cart storage
- Real-time cart updates
- Quantity management
- Automatic price calculation

### Order Processing
- Secure checkout form validation
- Customer data storage
- Order item tracking
- Automatic book availability updates

### Search & Filtering
- Full-text search
- Category filtering
- Real-time search results

### Responsive Design
- Mobile-first approach
- Bootstrap grid system
- Touch-friendly interface
- Optimized images

## Admin Panel Features

### Book Management
- Add/edit/delete books
- Upload book images
- Manage availability
- Category assignment

### Order Management
- View all orders
- Update order status
- Customer information
- Order details

### Category Management
- Create/edit categories
- Slug generation
- Category organization

## Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure form handling
- Environment variable configuration

## Performance Optimizations

- Database indexing
- Image optimization
- Lazy loading
- Efficient queries
- Static file compression

## Deployment Considerations

### Production Settings
- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Use environment variables
- Enable HTTPS
- Configure database properly

### Static Files
- Collect static files
- Configure CDN
- Enable caching
- Optimize assets

### Database
- Use production database
- Configure connection pooling
- Enable backups
- Monitor performance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please contact:
- Email: info@bookstore.com
- Website: https://bookstore.com

---

**Note**: This is a demonstration project. For production use, ensure proper security configurations and testing.
