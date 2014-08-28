.. _native-packages:

Why You Should Distribute Native Packages
=========================================

As a system administrator I deploy a lot of code. As web developer I
write a lot of code. Yet these two parts of me, are always at odds.

When working on web applications the system administrator in me says
"Just ship it!"

.. image:: _static/deployment/shipit.gif
    
While the web developer screams "It's not perfect yet!"

.. image:: _static/deployment/perfect.gif

And when the code finally gets deployed, things inevitably fall over in
the process.

.. image:: _static/deployment/unmaintain.gif

My years of experience being both a developer and system administrator
have taught me that the best way to distribute applications is by using
native packages.

Turning unmanagable deployments...

.. image:: _static/deployment/bad_package.gif

into well oiled machines.

.. image:: _static/deployment/good_package.gif

Native packages provide three major benefits over other deployment
strategies:

 #. Security
 #. Modularity
 #. Maintainability


Security
--------

The first benefit native package provide is security. This is an
optional benefit, as signing packages does not preclude them from being
deployed.

Every time I have to install `RVM <https://rvm.io>`_, I die a little
inside.

The RVM website provides a single method of installation:

.. code-block:: bash

 $ \curl -sSL https://get.rvm.io | bash -s stable

This is horribly insecure, dangerous, and the definition of `remote code
execution <https://en.wikipedia.org/wiki/Arbitrary_code_execution>`_.

Though RVM encourages installation over HTTPS, SSL is not enough
security for software distribution, because does not verify the
integrity of the content. 

By using signed native packages instead, you can verify two things:

 #. The package contents haven't changed since it was created.
 #. The package can only have come from the owner of the signing key.

This is because servers installing the package will already contain the
author's public key. 

Modularity
----------

Modularity is the second benefit native packages provide.

Native package create modularity by providing a clear distinction
between the build and deployment steps of a web application. This leads
to a highly scalable and continuously deployable application, which falls
in line with The `Twelve-Factor <https://12factor.net>`_ App definition.

Applications that don't have a clear distinction between these processes
tend to have deployments that organically grow into complex
monstrosities.

This complexity can be seen clearly around the upgrade and rollback
processes. Modularity comes from taking these processes and sectioning
them into before/after install and remove scripts. Instead of being ran
by an external process that requires elevated privileges to a production
server, these scripts - which are packaged with the application - execute
during upgrades (installing a new version) and rollbacks (downgrading
versions).

Maintainability
---------------

The final benefit native packages provide, is maintainability.

Instead of maintaining complex execution definitions or a plethora of
SCM resources in configuration management, system administrators have
only to write a few simple resources: install application, upload
configurations, restart services.

This leaves them with more time to fix important issues (like putting
out fires), and keeps them from having to spend multiple hours deploying
new versions.


Where it All Breaks Down
------------------------

Even with all these benefits, native packages are not a silver bullet.

A new (but simple) piece of infrastructure will need to be setup to host
package. If binaries are being signed, public keys will need to be
shipped with server images, and signing will need to be integrated into
the build processes. Migrating existing deployment architecture will
take time, along with the creation of packaging scripts.

And finally, multiple packages may need to be created for any server
that runs multiple versions of an application.


Concluding Remarks
------------------

If learning *rpmbuild* or *debuild* feel like it requires a robe and
wizard hat (because it surely does), tools like `fpm
<https://github.com/jordansissel/fpm>`_ make building packages extremely
simple.

Overall native package managers provide web application with greater
security, modularity, and maintainability. They also reduce deployment
times, and make system administrators lives easier. And even though they
introduce a new set of problems, theses can be resolved with few extra
resources and a little bit of time. The benefits of distributing native
packages far outweigh the costs, and will eventually save large amounts
time spent on development and administration.


Addendum: The Case for Language Specific Packages
-------------------------------------------------

Most modern languages (like Python, Ruby, Node.js, and Haskell), also
distribute their own package manager. If your web application is
written in one of these languages, consider using the language specific
package manager first. These provide versioning, dependency management,
and distribution.

But as soon configuration files, compiled assets, or any file that need
to be moved outside the directory after install, is required, start
transitioning to using native packages.
