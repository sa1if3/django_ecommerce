# Django Ecommerce/Market

Django E-commerce is a unique marketplace focused on enabling users to buy/sell products directly or request/send quotes without any complicated or exhaustive process. This is the open-source version of a larger project.

 ## Contents
 1. [Features](#features)
 1. [Installation](#installation)
    1. [Download the project](#download-the-project)
    1. [Set Virtual Environment](#set-virtual-environment )
    1. [Configure .ENV Settings](#configure-settings)
    1. [Async Tasks using Celery and Redis](#async-tasks-using-celery-and-redis)
    1. [Debug Toolbar](#debug-toolbar)
    1. [Migrate Database](#migrate-database)
    1. [Create a superuser](#create-a-superuser)
    1. [Collect static](#collect-static)
1. [Run Development Server](#run-development-server)
1. [First Run and Initial Data](#first-run-and-initial-data)
    1. [Admin Section](#admin-section)
    1. [User Section](#user-section)
1. [Order Process](#order-process)
1. [Credits](#credits)
1. [Screenshots](#screenshots)

### Features
1. User Panel
    1. User Management 
        - Sign Up
        - Log In
        - Email Password Reset
        - Email Verification
    1. Dashboard
    1. Item  
        - Search (Category / Name)
        - Buy Item
        - Request Quote
        - Orders
            - Placed By User
            - Placed By Customer
        - Quote
            - Placed By User
            - Placed By Customer
            - Upload Pdf
                - By Customer
                    - Purchase Order
                - By User/Seller 
                    - Quote 
                    - Invoice
                    - Delivery Receipt 
    1. Email Notifications: Enabled when `EMAIL_SEND = True` in `settings.py`
    1. SMS Notifications: Enabled when `SMS_SEND = True` in `settings.py`. [Pingsms API](https://pypi.org/project/pingsms-api/)
    1. Multiple Addresses: User addresses. One address can be set as default.
    1. Multiple Inventories: Each inventory must have an address.
    1. Item Listing: Each item is listed by against an inventory with visibility Public/Private.
    1. Shopping Cart
        - Checkout
        - TODO: Payment
    1. TODO: Chats and Notifications

1. Admin Panel
    1. Item Types
    1. Items
    1. Weight Groups
    1. Addresses
    1. Inventories
    1. Listings
    1. Orders
    1. Quotes
    1. Shopping Carts


## Installation
### Download the project
```bash
git clone https://github.com/sa1if3/django_ecommerce
``` 
or 

[Download ZIP](https://github.com/sa1if3/django_ecommerce/archive/refs/heads/main.zip)

### Set Virtual Environment 
Create a Virtual Environment
```bash
virtualenv venv
```

Activate Virtual Environment
```bash
source venv/bin/activate
```

Download Prerequisites using requirements.txt
```bash
pip install -r requirements.txt
```

Deactivate Virtual Environment
```bash
deactivate
```
### Configure Settings
Create a `.env` file in project folder `django_ecommerce` and provide values for the following variables. In case you are not using Email or SMS. Those fields can be left empty.

```python
SECRET_KEY=django-insecure-+_vcui795ns-2bl-$n)43ttpt6)s5s^2=t+8z*pv6%cqc*s)0i5
DB_NAME=
DB_USER=
DB_PASSWORD=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
PINGSMS_API_KEY=
PINGMS_SINGLE_SMS_TEMPLATE=
PINGMS_SENDER_ID=
```
### Async Tasks using Celery and Redis
Install Redis in Ubuntu 20.04 by following this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)

In `settings.py` set the following variables. Change according to your use case.

```python
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```

Activate Virtual Environment
```bash
source venv/bin/activate
```

Run Celery worker
```bash
celery -A django_ecommerce  worker -l info
```

[Note: In production, this command can be put in Supervisor]

### Debug Toolbar
If you are interested in using the debug toolbar make sure to change your `settings.py` file with the appropriate IP.

```python
DEBUG = True

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
```
### Migrate Database
The project uses PostgreSQL. Make sure your `settings.py` is set to correct credential.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'farmersmarket',
        'USER': 'farmersmarketuser',
        'PASSWORD': 'fkfQbfu6gnhGt',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

Section A of my [tutorial](https://techflow360.com/how-to-build-django-rest-api-with-oauth-2-0/) covers the setting up of a server part for Django development.

Run

```bash
python manage.py makemigrations
```
Followed by

```bash
python manage.py migrate
```

### Create a superuser
A superuser is required to access the admin panel located at `/accounts`

```bash
python manage.py createsuperuser
```
### Collect static
In case static files don't run properly simply run

```bash
python manage.py collectstatic
```

## Run Development Server
To start the project simply run the server with this command inside the activated virtual environment.
```bash
python manage.py runserver
``` 

## First Run and Initial Data
### Admin Section
Go to `http://yourdomain.com/accounts` and log in as a superuser. The admin needs to set up some initial data which restricts the user to sell items from the given category only. Enter data in the following order
1. Create Item Types: Type of item being sold
![Item Type](https://github.com/sa1if3/django_ecommerce/blob/main/Screenshots/item_type.PNG?raw=true)
1. Create Items: Each Item has an item type
![Item](https://github.com/sa1if3/django_ecommerce/blob/main/Screenshots/items.PNG?raw=true)
3. Create Weight Groups: Used during the listing, quote request and orders
![Weight Group](https://github.com/sa1if3/django_ecommerce/blob/main/Screenshots/weight_group.PNG?raw=true)

### User Section
A seller also needs to set up some initial data to list their items.
1. Create Address: Used for Inventory and invoices
1. Create Inventory: Used for Listing items. The name is shown to the buyer too.

1. Create Listing: List items for personal use view status as `Private` or public to view and purchase by setting the view status as `Public`. If all the items of a listing were sold off; the listing becomes automatically private and the seller is notified via email. The seller cannot search for their listings.

## Order Process

### Buy/Sell
1. Search
1. Add to Cart
1. Check Out
1. View Order Invoice

### Quotes
1. Search
1. Request Quote
1. Seller Uploads Quote
1. Buyer Uploads Purchase Order
1. Seller Uploads Invoice and Delivery Receipt

## Credits

[AdminLTE](https://adminlte.io/themes/v3/)

[unDraw](https://undraw.co/illustrations)

[pixabay](https://pixabay.com/)

## Screenshots
<table>
  <tr>
    <td>Sign Up</td>
     <td>Email Verification</td>
  </tr>
  <tr>
    <td><img src="Screenshots/Signup.PNG" width=600 height=250></td>
    <td><img src="Screenshots/email_verification.PNG" width=400 height=250></td>
  </tr>
  <tr>
    <td colspan="2">Dashboard</td>
  </tr>
  <tr>
    <td colspan="2"><img src="Screenshots/dashboard.PNG" width=1000 height=350></td>
  </tr>
  <tr>
    <td colspan="2">Search</td>
  </tr>
  <tr>
    <td colspan="2"><img src="Screenshots/search.PNG" width=1000 height=350></td>
  </tr>
  <tr>
    <td>Log In</td>
     <td>Address</td>
  </tr>
  <tr>
    <td><img src="Screenshots/login.PNG" width=600 height=250></td>
    <td><img src="Screenshots/address.PNG" width=400 height=250></td>
  </tr>
  <tr>
    <td>Checkout</td>
     <td>Inventory</td>
  </tr>
  <tr>
    <td><img src="Screenshots/checkout.PNG" width=600 height=250></td>
    <td><img src="Screenshots/Inventory.PNG" width=400 height=250></td>
  </tr>
 </table>

