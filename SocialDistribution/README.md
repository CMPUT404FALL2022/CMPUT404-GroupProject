#Django OpenShift v2

This git repository helps you get up and running quickly with django v1.7+ and Openshift.
###Features
* Ready to use for local development
* Easy to push to Openshift
* Works with  either PostgreSQL or MySQL
* Minimal changes to default django installation
* Names follow the django tutorial
* Uses new folder layout from Openshift March 2014 release
* Allows for debug mode on Openshift with the help of an environment variable.
* Use of static files is pre-configured

###How to use this repository
- Create an account at https://www.openshift.com
- Install the RHC client tools if you have not already done so.
```
sudo gem install rhc
rhc setup
```
- Create a Python 2.7 application
```
rhc app create django python-2.7
```
- Add the database cartridge (choose one)
```
rhc add-cartridge postgresql-9.2 --app django

OR

rhc add-cartridge mysql-5.5 --app django 
```
- Add this upstream repo
```
cd django
git remote add upstream -m master https://github.com/awwong1/openshift-django.git
git pull -s recursive -X theirs upstream master
```
- set the WSGI application to django's built in WSGI application (stored in the wsgi folder).
```
rhc env set OPENSHIFT_PYTHON_WSGI_APPLICATION=wsgi/wsgi.py --app django
```
- Push the repo upstream
```
git push
```
- SSH into the application to create a django superuser.
```
python app-root/repo/manage.py createsuperuser
```
- Now use your browser to connect to the Admin site.

### Static files
Static files are already setup and ready to use for either local or Openshift use. 

Place all static files / folders into the static folder.  They will be collected with collectstatic when pushed to openshift.

**DO NOT PUT STATIC FILES INTO /wsgi/static/**, this is merely a place holder for the collectstatic command.

### Where do I put my HTML Templates?
All your HTML templates should go into the /templates folder, and commited to your repository.  The settings.py setting is told to look here as a base starting point for all your .HTML files.

Django's standard is to put application level templates in a folder under the template folder, the same as the application name, but must be specified when calling it, i.e. TemplateView.as_view(template_name = "app1/myform.html"), but that is only a suggestion, not a hard and fast rule.  The tutorial has a good example for both static and template content. 

### Running locally and the django tutorial
This repository was designed to allow you to quickly develop and deploy a website to Openshift.  For local development, make sure you have the following setup:

- Virtualenv for this instance of python / django.
- pip (should be installed with virtualenv)

Once you have those installed, install the requirements for this repository:
```
pip install -r requirements.txt
```

This will install django on your local machine.

Once you have django installed, you can continue the tutorial from here https://docs.djangoproject.com/en/1.8/intro/tutorial01/#database-setup, although the default database and application configuration should be sufficient.

### Configuration details
When a git push is done, the .openshift/action_hooks/deploy is executed.  This script does two things:

1.  Runs python manage.py migrate to update any changes to the Schema
2.  Runs python manage.py collectstatic to move all necessary static files into /wsgi/static

#### Debugging mode and Openshift
By default, debug mode is off when pushed to Openshift.  However, if you'd like to turn on debugging (settings.DEBUG) while running on Openshift, you can set the environment variable DEBUG to True and then stop and start your application, and debugging will be turned on.

``` rhc env set DEBUG=True```

Once you are done debugging, set debug to a non-True value or remove it entirely.

``` rhc env unset DEBUG```

### HTTPS redirection
HTTPS redirection is accomplished by telling the local Apache gear to redirect all traffic to the HTTPS version of your site.  You'll need to add an .htaccess file into the WSGI folder

Add the following .htaccess file into the WSGI folder
```
RewriteEngine on  
RewriteCond %{HTTP:X-Forwarded-Proto} !https  
RewriteRule .* https://%{HTTP_HOST}%{REQUEST_URI} [R,L]  
```
This will redirect **ALL** HTTP traffic to the site to HTTPS.

### Notes on Python 3 compatibility
This has not been tested thoroughly with Python 3, and currently there is a bug with Python 3.3 on Openshift.

### Please Star if you like this repository.
I don't publish many repositories, but if you like this project, please star it, thanks.
=======
CMPUT404-project-socialdistribution
===================================

CMPUT404-project-socialdistribution

See project.org (plain-text/org-mode) for a description of the project.

Make a distributed social network!
