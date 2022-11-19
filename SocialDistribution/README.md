# Project setup

## Setting up a new environment
Before we do anything else we'll create a new virtual environment, using venv. This will make sure our package configuration is kept nicely isolated from any other projects we're working on.
```
python3 -m venv env
source env/bin/activate
```
## Install package requirements
Now that we're inside a virtual environment, we can install our package requirements.
```
pip install -r requirements.txt
```
## Run app
We're now ready to test the API we've built. Let's fire up the server from the command line.
```
cd SocialDistribution
python manage.py runserver
```
go to `http://127.0.0.1:8000/` if working on local host

# Learn more
## Django REST framework https://www.django-rest-framework.org/tutorial/quickstart/
## Uploading image https://dev.to/thomz/uploading-images-to-django-rest-framework-from-forms-in-react-3jhj


