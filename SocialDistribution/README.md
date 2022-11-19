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
```
cd SocialDistribution
python manage.py runserver
```
##
go to `http://127.0.0.1:8000/docs` if working on local host



