# BEST Deals API
## A web app that fetches the latest deals periodically from Jumia and souq and outputs them in the form of restful API
### check https://amir-best-deals.herokuapp.com for a live deployment
### Created by Amir Anwar
### amir.anwar.said@gmail.com

## Technologies used
Django

Django Rest Framework

Scrapy

Swagger API Documentation

## How to install locally

* clone git repo.

* create virtual environment beside the project folder:

    >`python3 -m venv venv`

* checkout your environment :
    > `source venv/bin/activate`
* install project requirements, from the project folder run:
    > `pip install -r requirements.txt`
* create your database (postgresql):
    
    open a new terminal
    
```
    sudo su postgres
    createuser --createdb --pwprompt bestdeals
    createdb -U bestdeals -W -h localhost best_deals
```

* you will be prompted for password twice, enter:

    >`bestdeals`

* now back to your first terminal where the virtual environment is activated

* migrate the db:

    >`python manage.py migrate`

* optional: create an admin account:

    >`python manage.py createsuperuser`

* **Now you are ready to run the app, we are NOT going to use the normal django way to run the server, Instead, run:**

    >`python project_entry.py`

* You are Done!


