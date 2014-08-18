You Should Be Using Native Packages
===================================

As a system administrator and web developer it's my job to write code,
deploy that code, and make sure that code stays running on servers.

Now these two parts of me, are always at odds.

The system administrator in me says "Just ship it!"

.. image:: _static/deployment/shipit.gif
    
While the web developer screams "It's not perfect yet!"

.. image:: _static/deployment/perfect.gif

Then there is the combination of the two that says, "That
deployment is so horrible to maintain!"

.. image:: _static/deployment/unmaintain.gif

Having been a system administrator and web developer for several years,
I have learned that deploying with git over ssh is just utterly
unmaintainable.


Git+SSH
-------

As a developer I understand where the mindset for deploying with git
comes from. The simplest way for to get an application on a server is
by using familiar tools.

Need to deploy the new version? Cool. Just ``ssh``, ``git pull``, run
migrations, and restart the webserver.

After the first deployment though, git+ssh starts to break down.

    New release? Okay ``git checkout --force``. Huh, files that were ``git
    rm``'ed are still around? Alright ``git clean -xdf``. Wait that just
    wiped out our local config, crap! Okay, let's just run the deploy
    script again.  Wait, that's not the right version. What do you mean
    we *just* released a new version?! GAAHH!!!

The main point is that this method breaks the `12factor`_ pattern for
scalable applications by merging the build and deploy steps.

Also, a lot of tooling ends up being written around having a clean
environment each time a new release comes out, along with scripts for
moving files, running migrations, creating users, and anything else
related to the deploy process.

    "But I *like* how easy my git deploys are! You, you boat rocker!"

Some still feel git and ssh is *the way* to deploy applications, and
that's fine, I won't stop them. But they should save themselves some
time and use an application like `git-deploy`_, or wrap things in
`fabric`_.

.. _12factor: http://12factor.net/build-release-run
.. _git-deploy: https://github.com/git-deploy/git-deploy
.. _fabric: http://fabric.rtfd.org


Language Package
----------------

So what's next? If git+ssh isn't the way to go, how should applications
be deployed? Well, the next logical thing after git based deploys are
building language specific packages. That means pip, npm, or rpm
installable packages.

Language specific packages allow developers to install and manage
versions of their code. They draw the distinction between building and
deploying applications. And for probably 90% of use-cases they are the
right way to go.

For the other 10% things get a little tricker. As soon as packages start
including resources not written in the language, packages start to show
their threads. When things like configuration files, static assets, and
binaries, are required for the application to run, language specific
packages don't cut it anymore.

If an application has reached this point, having a language specific
package can definitely still help, yet finding a better packaging
solution is paramount for maintainable deployments.

Tarballs
--------

Tarballs have been the default way to distribute software for quite some
time. Though they don't have any unified structure, they can include all
the resources a application needs to be deployed. Their integrity can easily be
verified using checksums.

On the downside, they represent a bootstrapping problem for deployments.
You need the deployment scripts, and the tarball, but the tarball
contains the deployment scripts. This leads to deployments being managed
by external tools such as Capestrano and Fabric, or even the rising
idiom of ``curl install.sh | bash``


Ideal World
-----------

My ideal world looks something like this:

.. code-block:: ruby

    package "Application" do
        version node['application']['version']
        action :install 
    end

    template "/etc/application/config.ini" do
        source "application.ini" 
        action :create
    end

    cookbook_file "/etc/init/application.conf" do
        source "application.conf"
        action :create
        notifies :restart, "service[application]", :delayed
    end

    service "application-cli" do
        supports :restart => true
        action [:enable, :start]
    end

For those not intimately familiar with Chef resources, this says: Install
application, upload the application configuration to
``/etc/application``, upload the webserver configuration to
``/etc/init/application.conf``, and start the application server using
``application-cli``.

In the real world though, install the package part ends up looking
something like my `racktables`_ deplyment config. A horrible mess of
unpacking a tarball, ensuring the checksum is correct, and extracting
files to the right place.

.. _racktables: https://github.com/osuosl-cookbooks/racktables/blob/v0.3.2/recipes/source.rb

Maybe, just maybe, there's a way we can get there.


native package
--------------

Cons:

* Multiple versions of same package (Drupal)

Breaks Down:

Requires native package server, which adds management overhead. If
signing binaries, need signing keys and infrastructure setup around
verification and key distribution (PKI). If pushing packages to OS
level, need designated maintainer, package needs to follow OS
guidelines, licensing issues, etc. 

Multiple versions of the same package can't be installed, without OS
level hacks like chroot, or rebuilding/renaming packages (or Arch).


Vision for Socorro
------------------

Right now I am interning at Mozilla and working on `Socorro`_: a distributed
system for collecting, analyzing, and viewing crash reports submitted
by `Breakpad`_. Part of my work involves making deployments of Socorro
`easier`_.

Socorro is installed by downloading a `deploy.sh` script on a server,
and pointing it to a tarball of Socorro. The tarball is downloaded,
extracted, and installed, while the deploy script does some heavy
lifting: ensuring dependencies are installed, creating users, setting
permissions, and copying around configuration files.

The deploy script does what most package managers do using *{pre,post}
install* scripts. My plan is to combine both the tarball and deploy
script into a single package using `fpm`_ so that deployments can be as
simple as:

.. code-block:: bash
    $ wget https://example.com/socorro.deb
    $ dpkg -i socorro.deb

.. _easier: https://bugzilla.mozilla.org/show_bug.cgi?id=1055268
.. _Breakpad: https://code.google.com/p/google-breakpad/
.. _Socorro: https://wiki.mozilla.org/Socorro
.. _fpm: https://github.com/jordansissel/fpm


Notes
=====

Native packages give you all the benefits of git based deploys, coupled
with the shippability of tarballs, the dependency injection of
language specific packages, and security.

They allow you to easily install software, copy over configs, and
rollback to previous versions.


`Ixiaus <https://news.ycombinator.com/item?id=5930109>`_ provided a
great, sadly minority, response to the HN article

https://hynek.me/articles/python-app-deployment-with-native-packages/
