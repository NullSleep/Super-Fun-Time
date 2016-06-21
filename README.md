# Super Fun Time

Basecamp time reports for the Zemoga App Dev team.

## Features

- Connection with the basecamp API.
- Real time updates.

## TO-DOs

- Make all ids and key parameters as environment variables.
- Django administration for all the users and data.
- Date selector.
- No-SQL database connection.

## Prerequisites

- Have [Python 2.7+](https://www.python.org) installed.
- Have [PostgreSQL 9.4+](https://www.postgresql.org) installed and running.

## How to Use

To use this project, follow these steps:

1. Create a working Python Virtual Environment (`$ virtualenv my_env`) navigate to it and activate it (`$ source bin/activate`)
2. Install Django (`$ pip install django -U`)
3. Clone the repository (`$ git clone https://github.com/NullSleep/Super-Fun-Time.git`) and navigate inside it.
4. Install the project requirements (`$ pip install -r requirements.txt`)
5. Collect the static files of the project (`$ python manage.py collectstatic`)
6. Set the PostgreSQL DB (see the PostgreSQL Database Configuration section)
7. Run the project (`$ python manage.py runserver`)

## PostgreSQL Database Configuration

To create a new database and user for the project do the following:

    $ psql
    $ CREATE DATABASE <db_name>;
    $ CREATE USER <db_user_name> WITH PASSWORD '<my_password>';

    $ ALTER ROLE <db_user_name> SET client_encoding TO 'utf8';
    $ ALTER ROLE <db_user_name> SET default_transaction_isolation TO 'read committed';
    $ ALTER ROLE <db_user_name> SET timezone TO 'UTC';

On the project settings.py change the DATABASES to this:

    $ DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '<db_name>',
            'USER': '<db_user_name>',
            'PASSWORD': '<my_password>',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

Migrate the database changes:

    $ python manage.py makemigrations
    $ python manage.py migrate

Make sure PostgreSQL is running before trying to run the project.

## Deployment to Heroku (only available to admins)

Make sure you have installed the [Heroku Toolbelt](https://toolbelt.heroku.com)

    $ git init
    $ git add -A
    $ git commit -m "Initial commit"

    $ heroku create
    $ git push heroku master

    $ heroku run python manage.py migrate

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
