release: python Instodramat/manage.py makemigrations; python Instodramat/manage.py makemigrations Users; python Instodramat/manage.py makemigrations Images; python Instodramat/manage.py migrate

web: gunicorn --pythonpath Instodramat Instodramat.wsgi