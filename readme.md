# Pure Beurre

Welcome to my 8th Project in OpenClassroom : Pure Beurre

## What is it?

It's an application where you can search for a specific french product and find an healthier substitute. You can also
save all of your favorite product and look at them at any time.

## Getting Started

You can use this application at : https://purebeurre-bn.herokuapp.com/

### Prerequistes

This application work with Python 3.7.3 and Django 3.0.5

This is set to use the default database of Django, but you're free to use your own SGDB and to configure it in settings.py

### Installing

Clone this repo 
```
git clone https://github.com/M0l42/P08_PureBeurre
```
Create the virtualenv

Install dependecies
```
pip install -r requirements.txt
```

Set the database and admin user
```
python manage.py migrate
python manage.py runscript load_database
python manage.py createsuperuser
```

Then you can run the app 
```
python manage.py runserver
```

## Built With

* [Django](https://www.djangoproject.com/)
* [Start Bootstrap Template](https://startbootstrap.com/themes/creative/)
* [OpenFoodFacts](https://fr.openfoodfacts.org/)
