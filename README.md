# social-media-server [![Build Status](https://travis-ci.org/dowrow/social-media-server.svg?branch=master)](https://travis-ci.org/dowrow/social-media-server)
RESTfull API for a social media platform  based on Django 1.9.

Continuous Integration with: http://social-media-server.herokuapp.com

## Dependencies

- Django
- Django Rest Framework
- Django Social OAuth2

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
