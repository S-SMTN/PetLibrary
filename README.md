# PetLibrary

PetLibrary is a multi-tenant library management REST service built with Django and **django-tenants**. 

## Features

- **Multi-tenancy** – each library is isolated within its own subdomain.
- **Book Borrowing System** – tracks book checkouts and returns, including overdue calculations.
- **Stripe Integration** – each library can process payments using a global Stripe account.
- **Django Debug Toolbar** – debugging and performance monitoring.
- Administrators can populate the library with generated book records (including authors) and users (10 at a time) via a POST request to a specific endpoint. This uses Faker and Factory Boy technologies to generate random data.
- Ability to run **PostgreSQL Admin (pgAdmin)** locally using Docker Compose for easier database management.

## Technologies & Dependencies

- **Python** (3.12)
- **Django** (5.1.2)
- **Django REST Framework** (3.15.2)
- **PostgreSQL** - default database hosted on AWS, but can be set up elsewhere
- **django-tenants** (3.7.0) - for multi-tenancy management
- **django-debug-toolbar** (4.4.6) - for debugging and profiling
- **djangorestframework-simplejwt** (5.3.1) - for JWT-based authentication
- **stripe** (11.1.1) - for payment processing
- **factory_boy** (3.3.1) - for generating fake data in tests
- **Faker** (30.3.0) - for generating random data (e.g., book titles, author names)
- **psycopg2-binary** (2.9.9) - for PostgreSQL database connection
- **python-dotenv** (1.0.1) - for loading environment variables from `.env` files
- **Docker Compose** - for running PostgreSQL Admin (pgAdmin) locally
- **drf-spectacular** (0.28.0) - for generating API documentation

## Installation & Setup

### 1. Clone the Repository

```sh
 git clone https://github.com/S-SMTN/PetLibrary
```

### 2. Navigate to the project folder:
```sh
 cd PetLibrary
```

### 3. Create and Activate Virtual Environment

```sh
 python -m venv venv
 source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```sh
 pip install -r requirements.txt
```

### 5. Configure Database

By default, the project is configured to use a PostgreSQL database hosted on AWS. You can either use this cloud database or configure a different PostgreSQL instance on another platform.
Provide connection details in `.env`:

```env
DB_Link=YOUR_DB_LINK
DB_Password=YOUR_DB_Password
DB_User=YOUR_DB_User
DB_Name=YOUR_DB_Name
```

### 6. Create a Stripe account:

You need to create a Stripe account to handle payments. Follow these steps:

#### 1. Go to [Stripe](https://stripe.com) and sign up for an account.

#### 2. After creating your account, obtain the `Stripe Secret Key` and `Stripe Publishable Key` from the Stripe dashboard.

#### 3. Set the obtained keys as environment variables into `.env` file):

```env
STRIPE_SECRET_KEY=YOUR_STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY=YOUR_STRIPE_PUBLISHABLE_KEY
STRIPE_WEBHOOK_SECRET=YOUR_STRIPE_WEBHOOK_SECRET
```

### 7. Configure and run Docker Compose to start PostgreSQL Admin (pgAdmin) locally:

If you need to manage your PostgreSQL database through a web interface, you can use Docker Compose to run pgAdmin:

#### 1. Provide connection details in `.env`:

```env
PGADMIN_EMAIL=YOUR_PGADMIN_EMAIL
PGADMIN_PASSWORD=YOUR_PGADMIN_PASSWORD
```

#### 2. Ensure Docker and Docker Compose are installed on your machine.

#### 3. In the project root, run:

```env
docker-compose up
```
#### 4. Access pgAdmin at http://localhost:5050, log in using the credentials specified in the `.env` file.

### 8. Apply Migrations

```sh
 python manage.py migrate_schemas --shared
```

### 9. Create a superuser:

```sh
 python manage.py createsuperuser
```
Follow the prompts to create the superuser account.

### 10. Start the development Server

#### 1. In your `.env` file, ensure the `DOMAIN_NAME` variable is set to the desired domain (`localhost` may be used on the development Server):

```env
DOMAIN_NAME=localhost
```

#### 2. Start the development server with the following command:

```sh
 python manage.py runserver $DOMAIN_NAME:8000
```

Access the app at `http://$DOMAIN_NAME:8000`.

## API Usage

### 1. Obtain JWT credentials:

To access the API, you first need to obtain a JWT token. Make a POST request to the following endpoint: `http://$DOMAIN_NAME:8000/api/user/token/`

Pass the following parameters in the request:

- `username`
- `password`

This will return a JWT token that you can use to authenticate further requests.

### 2. Use the JWT token:

Once you have the token, include it in the `Authorization` header of your API requests like this:

```http
Authorization: Bearer <your-jwt-token>
```

### 3. Create a Library Tenant:

Send a POST request to the following endpoint: `http://$DOMAIN_NAME:8000/api/library/`

Include the following parameters in the request body:

- `name`: The name of the library.
- `subdomain`: A unique subdomain for the library.
- `address`: The address of the library.

This will create a library tenant for your project.

Example POST request body:

```json
{
  "name": "My Library",
  "subdomain": "my-library",
  "address": "123 Library St, City"
}
```

Once the request is successful, a new library tenant will be created, and you can access the library using the specified subdomain. For example: `http://$SUBDOMAIN.$DOMAIN_NAME/api/books/`, `http://$SUBDOMAIN.$DOMAIN_NAME/api/borrowings/`, `http://$SUBDOMAIN.$DOMAIN_NAME/api/payments/`

### 4. Optional: Generate Fake Data

If you need to quickly generate fake data for books and borrowings, you can use the following endpoints:

#### 1. Generate fake books:

Send a POST request without parameters to the following endpoint: `http://$SUBDOMAIN.$DOMAIN_NAME/api/book_factory/`

This will create 10 fake book records and return all created records.

#### 2. Generate fake borrowings:

Send a POST request without parameters to the following endpoint: `http://$SUBDOMAIN.$DOMAIN_NAME/api/borrowing_factory/`

This will create 10 fake borrowing records and return all created records.

## API documentation:

API documentation has been integrated into the project. You can access it using the following tools:

### 1. Swagger UI:

View and interact with the API documentation through Swagger UI at: `http://$DOMAIN_NAME:8000/swagger/`

### 2. ReDoc:

A clean, interactive documentation is available through ReDoc at: `http://$DOMAIN_NAME:8000/redoc/`

## License

MIT License. Free to use and modify.

