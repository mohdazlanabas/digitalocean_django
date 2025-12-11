# Django Hello World - Step-by-Step Guide

## What We Built

A simple Django web application that displays "Hello World" on a webpage.

## Step-by-Step Instructions

### Step 1: Install Django
```bash
pip3 install django --break-system-packages
```

This installs Django, the web framework we're using.

### Step 2: Create Django Project
```bash
django-admin startproject helloworld_project
cd helloworld_project
```

This creates the main project structure with configuration files.

**What gets created:**
- `manage.py` - Command-line utility for Django
- `helloworld_project/` - Main project directory
  - `settings.py` - Project configuration
  - `urls.py` - URL routing
  - `wsgi.py` & `asgi.py` - Deployment files

### Step 3: Create Django App
```bash
python3 manage.py startapp hello
```

Django projects contain "apps" - modular components. This creates the `hello` app.

**What gets created:**
- `hello/` - App directory
  - `views.py` - Where we define our page logic
  - `models.py` - Database models (not used in this example)
  - `admin.py` - Admin interface config
  - `apps.py` - App configuration
  - `tests.py` - Unit tests

### Step 4: Create the View
Edit `hello/views.py`:
```python
from django.shortcuts import render
from django.http import HttpResponse

def hello_world(request):
    """Simple view that returns Hello World"""
    return render(request, 'hello/index.html')
```

A **view** is a Python function that takes a web request and returns a web response.

### Step 5: Create URL Configuration for the App
Create `hello/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
]
```

This tells Django: "When someone visits the root URL, call the hello_world view."

### Step 6: Include App URLs in Project
Edit `helloworld_project/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello.urls')),
]
```

This connects your app's URLs to the main project.

### Step 7: Register the App
Edit `helloworld_project/settings.py`, add 'hello' to INSTALLED_APPS:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello',  # Add this line
]
```

This tells Django your app exists and should be loaded.

### Step 8: Create Template Directory
```bash
mkdir -p hello/templates/hello
```

Django looks for templates in `templates/` directories within each app.

### Step 9: Create HTML Template
Create `hello/templates/hello/index.html` with your HTML content.

Templates are HTML files that Django can render dynamically.

### Step 10: Run the Development Server
```bash
python3 manage.py runserver
```

This starts Django's built-in development server at `http://127.0.0.1:8000/`

### Step 11: View Your Site
Open your browser and go to `http://127.0.0.1:8000/`

You should see "Hello World!" displayed on the page.

## Django Project Structure Explained

```
helloworld_project/
├── manage.py                          # Command-line utility
├── helloworld_project/                # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # Settings (database, apps, etc.)
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py                        # WSGI deployment
│   └── asgi.py                        # ASGI deployment
└── hello/                             # Your app
    ├── __init__.py
    ├── admin.py                       # Admin interface
    ├── apps.py                        # App configuration
    ├── models.py                      # Database models
    ├── views.py                       # View functions
    ├── urls.py                        # App-specific URLs
    ├── tests.py                       # Unit tests
    ├── migrations/                    # Database migrations
    └── templates/                     # HTML templates
        └── hello/
            └── index.html
```

## Key Django Concepts

1. **Project vs App**: A project contains multiple apps. Apps are reusable components.

2. **MTV Pattern** (Model-Template-View):
   - **Model**: Data structure (we didn't use one here)
   - **Template**: HTML presentation layer
   - **View**: Business logic that connects models and templates

3. **URL Routing**: Maps URLs to views
   - Main project `urls.py` includes app `urls.py`
   - App `urls.py` maps specific paths to views

4. **Templates**: HTML files with Django template language
   - Located in `templates/` directory
   - Can use variables, loops, conditionals

## Common Django Commands

```bash
# Create new project
django-admin startproject projectname

# Create new app
python3 manage.py startapp appname

# Run development server
python3 manage.py runserver

# Run on different port
python3 manage.py runserver 8080

# Create database migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate

# Create superuser for admin
python3 manage.py createsuperuser
```

## Next Steps

To expand this application, you could:
1. Add more views and URLs
2. Create models for database interaction
3. Use Django's admin interface
4. Add static files (CSS, JavaScript, images)
5. Implement forms and user input
6. Connect to a PostgreSQL database
7. Deploy to production

## Troubleshooting

**Port already in use?**
```bash
python3 manage.py runserver 8080
```

**Template not found?**
- Check that 'hello' is in INSTALLED_APPS
- Verify template path: `hello/templates/hello/index.html`
- Django looks in `appname/templates/appname/` by convention

**Module not found?**
- Make sure you're in the project directory with `manage.py`
- Check that Django is installed: `pip3 list | grep Django`
