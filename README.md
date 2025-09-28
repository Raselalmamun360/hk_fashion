# HK Fashion E-commerce Project

A simple Django e-commerce project for a fashion store with cash on delivery payment method and pre-order functionality.

## Features

- Product browsing and searching
- Product categories
- Product detail pages
- Pre-order functionality
- Shopping cart
- User registration and authentication
- User profiles
- Order management
- Cash on delivery payment method
- Responsive design with Bootstrap

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hk_fashion
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the site at http://127.0.0.1:8000/

## Project Structure

- **products**: App for managing products and categories
- **cart**: App for shopping cart functionality
- **orders**: App for order processing and management
- **users**: App for user authentication and profiles

## Admin Access

Access the admin panel at http://127.0.0.1:8000/admin/ using the superuser credentials created earlier.

## Testing

Run the tests using the provided script:
```bash
./run_tests.sh
```

Or run individual test modules:
```bash
python manage.py test products
python manage.py test cart
python manage.py test orders
python manage.py test users
```

## Adding Products

1. Log in to the admin panel
2. Create categories
3. Add products to the categories
4. Set the "is_preorder" flag for pre-order items

## License

This project is licensed under the MIT License.