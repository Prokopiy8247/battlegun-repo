# Technical Specification: Battlegun - Airsoft Equipment E-commerce Platform

## 1. Project Overview

**Project Name:** Battlegun  
**Purpose:** E-commerce platform for selling airsoft equipment and accessories  
**Language:** English (UI and content)

## 2. Technology Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | Django 5.x |
| Database | PostgreSQL 16 |
| CSS Framework | Tailwind CSS 3.x |
| Frontend Interactivity | HTMX 2.x |
| Client-side JS | Alpine.js 3.x |
| Containerization | Docker & Docker Compose |
| Web Server / Reverse Proxy | Nginx |
| Payment Gateway | NOWPayments API |

## 3. Project Structure

```
battlegun/
├── docker-compose.yml
├── Dockerfile
├── nginx/
│   └── nginx.conf
├── manage.py
├── config/                     # Django settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── catalog/                # Products, Categories
│   ├── cart/                   # Shopping cart
│   ├── orders/                 # Order management
│   └── payments/               # NOWPayments integration
├── core/                       # Base classes, mixins, utils
├── services/                   # Business logic layer
├── templates/
│   ├── base.html
│   ├── components/             # Reusable HTMX components
│   ├── catalog/
│   ├── cart/
│   └── orders/
├── static/
│   ├── css/
│   └── js/
├── media/                      # User uploaded files
├── requirements.txt
├── .env.example
└── README.md
```

## 4. Functional Requirements

### 4.1 Product Catalog

#### Features:
- Display products in a grid layout with pagination
- Category-based filtering (HTMX-powered, no page reload)
- Product search functionality
- Sorting options (price, name, newest)
- Product availability status

#### Product Attributes:
- Name, SKU, Slug
- Description (short and full)
- Price, Discount price (optional)
- Category (hierarchical)
- Images (multiple, with primary image)
- Stock quantity
- Specifications (key-value pairs)
- Status (active/inactive)
- Timestamps

#### Categories:
- Hierarchical structure (parent-child)
- Category image
- SEO-friendly slugs
- Active/inactive status

### 4.2 Product Detail Page

#### Features:
- Large product images with gallery
- Full product description
- Specifications table
- Price display (with discount if applicable)
- Stock availability indicator
- Add to cart button with quantity selector
- Related products section

### 4.3 Shopping Cart

#### Features:
- Modal window implementation (Alpine.js)
- Add/remove products
- Update quantities
- Display subtotal and total
- Persistent cart (session-based for guests)
- Cart icon with item count in header
- HTMX-powered updates without page reload

### 4.4 Order Management

#### Features:
- Checkout form with customer information
- Order summary display
- Order confirmation page
- Order status tracking

#### Order Data:
- Order number (unique)
- Customer information (name, email, phone)
- Shipping address
- Order items (snapshot of products)
- Subtotal, shipping, total
- Status (pending, paid, processing, shipped, delivered, cancelled)
- Payment reference
- Timestamps

### 4.5 Payment Integration (NOWPayments)

#### Features:
- Cryptocurrency payment support
- Payment status webhook handling
- Payment confirmation
- Automatic order status update upon successful payment

## 5. Non-Functional Requirements

### 5.1 Security

- CSRF protection on all forms
- SQL injection prevention (Django ORM)
- XSS protection (template auto-escaping)
- Secure headers configuration
- HTTPS enforcement in production
- Environment variables for sensitive data
- Input validation and sanitization
- Webhook signature verification (NOWPayments)

### 5.2 Code Quality Standards

#### OOP Principles:
- SOLID principles adherence
- Clean separation of concerns

#### DRY (Don't Repeat Yourself):
- Reusable template components
- Base classes and mixins in `core/`
- Shared business logic in `services/`
- Template inheritance

#### Architecture Patterns:
- Service Layer Pattern for business logic
- Fat Models, Thin Views approach
- Reusable mixins and base classes

#### Best Practices:
- Type hints throughout codebase
- Meaningful variable and function names
- Proper exception handling
- Database query optimization

### 5.3 SPA-like Experience (HTMX)

- All catalog filtering without page reload
- Cart operations via HTMX requests
- Partial page updates
- Loading indicators
- URL updates with `hx-push-url`
- Browser history support

## 6. Data Models

### 6.1 Category
```
Category
├── id: UUID (PK)
├── name: CharField(100)
├── slug: SlugField(unique)
├── description: TextField (nullable)
├── image: ImageField (nullable)
├── parent: ForeignKey(self, nullable)
├── is_active: BooleanField(default=True)
├── sort_order: PositiveIntegerField(default=0)
└── timestamps
```

### 6.2 Product
```
Product
├── id: UUID (PK)
├── name: CharField(200)
├── slug: SlugField(unique)
├── sku: CharField(50, unique)
├── description_short: CharField(500)
├── description: TextField
├── price: DecimalField(10, 2)
├── discount_price: DecimalField (nullable)
├── category: ForeignKey(Category)
├── stock: PositiveIntegerField(default=0)
├── is_active: BooleanField(default=True)
└── timestamps
```

### 6.3 ProductImage
```
ProductImage
├── id: UUID (PK)
├── product: ForeignKey(Product)
├── image: ImageField
├── alt_text: CharField(200)
├── is_primary: BooleanField(default=False)
└── sort_order: PositiveIntegerField
```

### 6.4 ProductSpecification
```
ProductSpecification
├── id: UUID (PK)
├── product: ForeignKey(Product)
├── name: CharField(100)
└── value: CharField(200)
```

### 6.5 Cart
```
Cart
├── id: UUID (PK)
├── session_key: CharField(40)
└── timestamps
```

### 6.6 CartItem
```
CartItem
├── id: UUID (PK)
├── cart: ForeignKey(Cart)
├── product: ForeignKey(Product)
├── quantity: PositiveIntegerField(default=1)
└── price: DecimalField(10, 2)
```

### 6.7 Order
```
Order
├── id: UUID (PK)
├── order_number: CharField(20, unique)
├── email: EmailField
├── first_name: CharField(50)
├── last_name: CharField(50)
├── phone: CharField(20)
├── address: TextField
├── city: CharField(100)
├── postal_code: CharField(20)
├── country: CharField(100)
├── subtotal: DecimalField(10, 2)
├── shipping_cost: DecimalField(10, 2)
├── total: DecimalField(10, 2)
├── status: CharField(20)
├── notes: TextField (nullable)
└── timestamps
```

### 6.8 OrderItem
```
OrderItem
├── id: UUID (PK)
├── order: ForeignKey(Order)
├── product: ForeignKey(Product)
├── product_name: CharField(200)
├── product_sku: CharField(50)
├── price: DecimalField(10, 2)
├── quantity: PositiveIntegerField
└── subtotal: DecimalField(10, 2)
```

### 6.9 Payment
```
Payment
├── id: UUID (PK)
├── order: OneToOneField(Order)
├── payment_id: CharField(100)
├── payment_status: CharField(50)
├── pay_address: CharField(200)
├── pay_amount: DecimalField(18, 8)
├── pay_currency: CharField(10)
├── price_amount: DecimalField(10, 2)
├── price_currency: CharField(10)
└── timestamps
```

## 7. URL Endpoints

### Catalog
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Home page |
| GET | `/catalog/` | Product catalog |
| GET | `/catalog/<category_slug>/` | Products by category |
| GET | `/product/<slug>/` | Product detail |

### Cart (HTMX)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/cart/` | Cart modal content |
| POST | `/cart/add/<product_id>/` | Add to cart |
| POST | `/cart/update/<item_id>/` | Update quantity |
| DELETE | `/cart/remove/<item_id>/` | Remove item |
| GET | `/cart/count/` | Cart count |

### Orders
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/checkout/` | Checkout page |
| POST | `/checkout/` | Create order |
| GET | `/order/<order_number>/` | Order confirmation |

### Payments
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/payment/create/<order_id>/` | Create payment |
| POST | `/payment/webhook/` | NOWPayments IPN |

## 8. Environment Variables

```env
# Django
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

# Database
DATABASE_URL=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

# NOWPayments
NOWPAYMENTS_API_KEY=
NOWPAYMENTS_IPN_SECRET=
```

## 9. Docker Services

- **web**: Django application (Gunicorn)
- **db**: PostgreSQL database
- **nginx**: Reverse proxy and static files

## 10. Development Setup

1. Clone repository
2. Copy `.env.example` to `.env`
3. Run `docker-compose up -d`
4. Run migrations
5. Create superuser
6. Access at `http://localhost:8000`