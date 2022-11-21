# Where do I put my HTML Templates?
All your HTML templates should go into the /templates folder, and commited to your repository. The settings.py setting is told to look here as a base starting point for all your .HTML files.

Django's standard is to put application level templates in a folder under the template folder, the same as the application name, but must be specified when calling it, i.e. TemplateView.as_view(template_name = "app1/myform.html"), but that is only a suggestion, not a hard and fast rule. The tutorial has a good example for both static and template content.
##bootrap
## What is bootstrap
Bootstrap is a free and open-source CSS framework directed at responsive, mobile-first front-end web development. It contains HTML, CSS and (optionally) JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.
[View on Github](https://github.com/twbs/bootstrap/blob/v5.2.2/site/content/docs/5.2/getting-started/introduction.md).
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
### To learn Django REST framework, checkout https://www.django-rest-framework.org/tutorial/quickstart/
### To learn Uploading image, checkout https://dev.to/thomz/uploading-images-to-django-rest-framework-from-forms-in-react-3jhj
### To learn bootstrap, checkout https://getbootstrap.com/docs/5.2/getting-started/introduction/
### To learn HTML, checkout https://developer.mozilla.org/en-US/docs/Web/HTML



