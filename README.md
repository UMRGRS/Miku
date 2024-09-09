# Miku!

This is a personal project using Django and Django REST framework, it consists of multiple apps with different uses

## Current apps

### Users

An app used for authentication and authorization for the other apps in the project

### Binnacle NSO

A simple binnacle with some custom features :3

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/UMRGRS/Miku-.git
    $ cd Miku-
    
Create and activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
Then simply apply the migrations:

    $ python manage.py migrate

This projects requires you to have Redis installed and running on port 6379, you can install it here:

https://redis.io/docs/latest/get-started/

You can now run the development server:

    $ python manage.py runserver

Then start huey to run scheduled tasks:

    $ python manage.py run_huey
