# flask-sqlalchemy

### Basics

1. Fork/Clone
2. Activate a virtualenv (if you don't want to mess up packages:))
3. Install the requirements

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database flask-test
# \q

```

Create the tables and run the migrations:

```sh
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

### Run the Application

```sh
$ python manage.py runserver
```

### Code Quality
Go to the project directory:
```sh
$ pylint --load-plugins pylint_flask_sqlalchemy src

```
