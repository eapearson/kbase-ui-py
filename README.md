# KBase UI - Django Flavored

## Running it

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd django
python manage.py runserver
```

## Design

A django web app without a database!

Views define all data access.

Much more to come with experience.

## Tasks

### Run Server

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd django
python manage.py runserver
```

```bash
docker network create kbase-dev
ENV=ci docker-compose up
```

### Add App

We use one app per major, top-level, path destination.

1. create the app

   ```bash
   cd django
   python manage.py startapp APPNAME
   ```

2. create the templates directory

   ```bash
   mkdir -p APPNAME/templates/APPNAME
   ```

3. Create `APPNAME/templates/APPNAME/index.html`

   with

   ```django
   {% extends "base.html" %}

   {% block content %}

   YOUR CONTENT HERE

   {% endblock content %}
   ```

4. Create the views

   edit `APPNAME/views.py`

   add

   ```python
   from django.shortcuts import render
   def index(request):
       return render(request, 'APPNAME/index.html',
        {"page": {"title": "APP TITLE"}, 
        "kbase": request.kbase},)

   ```

   Note that:

   - `page` is used to set page level variables, in this case just the title, which is displayed in the header
   - `kbase` carries data set by KBase middleware, such as auth, and enables authentication and configuration

5. Create `APPNAME/urls.py`

   with the content

   ```python
   from django.urls import path

   from . import views

   urlpatterns = [
       path('', views.index, name='index'),
   ]
   ```

6. Add base url for app to `kbase_ui_py/urls.py`

   ```python
   path('MYAPP/', include('MYAPP.urls')),
   ```

7. Add to `settings.py`

   Add an entry to `INSTALLED_APPS`:

   ```python
   'MYAPP.apps.MyappConfig',
   ```

   This matches the file `MYAPP/apps.py` inside of which you'll find a class generated `MyappConfig`, where `Myapp` is the proper-cased version of the app name.

#### With a url parameter

### Add view to an app

### Passing data to a view
