.. _deploying-django-is-hard:

Why Deploying Django Is Hard
============================

The easiest way to deploy a python application, is with python's own
package management tool: pip.

The problem with Django, is that this works great for Django
applications, it doesn't work at all for Django projects.

This is my tale of trying to wrestle the Socorro django project
'crashstats' into a deployable state, and how I ultimately failed.

.. note:: From now on I will refer to the directory at
    `socorro/webapp-django` as `crashstats`.


setup.py
--------

The first part of making glob of python code into a python package is
`setup.py`. Thankfully, crashstats already had a setup.py. Un-thankfully
it contained very little that was helpful in packaging up the project. 

After bringing the file up to current packaging standards (including the
README in description, listing install_requires, etc.) I was able to
`python setup.py install` the project.

This was a good step forward, but there were still two things
missing. (In hindsight there are more than two, but these are the
biggest problems) First, the ability to run the manage.py script outside of the
install directory of the application. Second, having settings.py
exist outside the install directory.

.. sidebar:: The other issues were installing the wsgi file somewhere
    else, and being able to call 'collectstatic' and 'compress' with
    directory arguments.


Where It All When Wrong: manage.py
----------------------------------

Django projects are created by running `django-admin.py createproject`.
This creates a manage.py file, a directory for other applications, and a
urls.py file. This is all pretty standard, except when you use
Playdoh.

Playdoh, by which people mean Funfactory, is a project written by
Mozilla in search of a standard, secure, sanely defaulted, Django
project template. One of the things funfactory does when creating a new
project, is generate a different manage.py than the default Django one.

This is because funfactory include's some of it's own management code,
so that things like having a base.py settings file with the ability to
override it in local.py is simple to setup.

The problem with this is that it overrides the default way Django does
things, and also is not kept up to date with Django. (They changed a bit
of how manage.py works and how settings are loaded between 1.4 and 1.5)

Part of this is that funfactory uses the location of manage.py to
determine where the rest of the project lies. This doesn't work at all
if you say, want to move manage.py into a script directory so that you
can actually ship it in the python package.

See Python has a feature called 'console_scripts'. These allow you to
setup python scripts as binary. Much like pep8, gunicorn, and other
python projects work. The problem with this is that console_scripts rely
on scripts existing within a python module. (Is this really true? I
don't know if I tried just using manage.py [manage:main] or [:manage]?)

One option is to use the `scripts` keyword for setup, but this will
install a binary called `manage.py` to `bin` under the virtualenv. Still
not what we want.

A List Of Demands
-----------------

What does the end result look like?

/etc/project/myproj.wsgi
/etc/project/settings.ini
/usr/bin/project-script
