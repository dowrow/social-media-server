# social-media-server [![Build Status](https://travis-ci.org/dowrow/social-media-server.svg?branch=master)](https://travis-ci.org/dowrow/social-media-server)
RESTfull API for a social media platform  based on Django 1.9.

## Continuous Integration


This repo is synchronized with Heroku:[http://social-media-server.herokuapp.com](http://social-media-server.herokuapp.com)

## Dependencies

- [Django](https://github.com/django/django)
- [Django Rest Framework](https://github.com/tomchristie/django-rest-framework)
- [Django Rest Social OAuth2](https://github.com/PhilipGarnero/django-rest-framework-social-oauth2)

## Deployment to Heroku
Run:

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
