# DiaryProducts E-commerce Website

Welcome to the DiaryProducts E-commerce website, a meticulously crafted platform for all your dairy product needs. Our goal is to provide you with a seamless and enjoyable shopping experience. This website is powered by Python Django, HTML, CSS, JavaScript, and Bootstrap, ensuring a robust and user-friendly interface.

Check the website in :  www.diaryproducts.shop 

## Features

### User Authentication and Profile Management

- Secure login and registration pages with email authentication.
- Forgot password functionality for easy account recovery.
- User profile page with the ability to add and manage multiple delivery addresses.
- Update or edit address details directly from the user profile page.

### Product Management

- Home page showcasing a wide variety of dairy products.
- Detailed product pages for in-depth information.
- Navbar with a separated product list for easy filtering.

### Navigation and Pages

- About Us and Contact pages to provide additional information.
- Search bar for quick product search.
- Cart page displaying total products, quantities, unit prices, and total prices.

### Checkout and Payment

- Seamless checkout process with a secure payment button.
- Payment processed through Razorpay for a smooth transaction.
- Order history and status page after successful payment completion.

## Admin Portal

Take control of the database and perform necessary operations through the built-in Django admin portal.

## Hosting Information

The DiaryProducts E-commerce website is hosted on AWS. To set up the project locally, consider the following:


### Prerequisites

Ensure you have the following installed on your local machine:

- [Python](https://www.python.org/downloads/) (version 3.6 or higher)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Virtualenv](https://pypi.org/project/virtualenv/)

### Clone the Repository

```
git clone https://github.com/yourusername/diaryproducts-ecommerce.git
cd diaryproducts-ecommerce

```
### Set Up Virtual Environment

```
# On Windows
python -m venv venv
# On macOS and Linux
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS and Linux
source venv/bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt

```




### Environment Configuration

In your `.env` file, provide your own generated secret keys.

```env
SECRET_KEY=your_secret_key
DEBUG=True
```
#### Script Configuration

Update the fields in the script area of your Django project:
```
# settings.py

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your_domain_here']

# Django 4.0+ CSRF Configuration
CSF_TRUSTED_ORIGINS = ['your_domain_here']
```
Also in static in js file , in  " myscripts.js " change  local host to your domain if it is hosted:
```
 window.location.href = `http://localhost:8000/product-detail/${id}`
```
to 
```
 window.location.href = `"your domain" /product-detail/${id}`
```


### Run Migrations
```
python manage.py migrate
```
### Create Superuser (Admin Account)

```
python manage.py createsuperuser
```
Follow the prompts to create an admin account for the Django admin portal.

### Run the Development Server
```
python manage.py runserver
```
Visit http://localhost:8000/ in your browser to explore the DiaryProducts E-commerce website locally.

## Reminder
Don't forget to keep your secret keys confidential and ensure proper configuration for a secure and smooth operation. 

For more details, refer to the official Django documentation.

## Contact and Collaboration
For any inquiries, collaboration opportunities, or feedback, please contact me at sidhub41214@gmail.com. We value your input and look forward to serving you better.

For contributions and bug reports, feel free to open an issue or submit a pull request on our GitHub repository.

Thank you .



