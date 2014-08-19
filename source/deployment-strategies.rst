You Should Be Using Native Packages
===================================

As a system administrator and web developer it's my job to write code,
deploy that code, and make sure that code stays running on servers.

These two parts of me, are always at odds.

The system administrator in me says "Just ship it!"

.. image:: _static/deployment/shipit.gif
    
The web developer screams "It's not perfect yet!"

.. image:: _static/deployment/perfect.gif

While the devop just cries at the lack of idempotency.

.. image:: _static/deployment/unmaintain.gif

Having deployments that are simple, easy, and quick, provides more time
for development, and administration. But getting an application to that
point can require a lot of time.

In my experience, an application follows this progression for
deployments:

 1. Git+SSH
 2. Language Package
 3. Tarballs
 4. Native Packages

Hopefully by the end of this document you will understand how to get
your deployment from this:

.. image:: _static/deployment/bad_package.gif

To this:

.. image:: _static/deployment/good_package.gif


Git+SSH
-------

When you have a hammer as a developer, its always easy to see every
problem as a nail. This is where the mindset of using git and ssh for
deployments come from.

git+ssh allow developers to quickly and easily get their code up and
running on another machine, but it comes at a cost.

Applications require more than just the code to run:

 * configuration files
 * database migrations
 * static assets
 * initialization scripts

And after the first deployment, git+ssh starts to break down, and more
and more tooling gets added to copy files, run migrations, restart
servers, and upload assets. This breaks the `12factor`_ pattern of
seperating the build and deploy processes.

At some point in the application's lifecycle a rollback will have to
happen, and this will add even more complexity.

Tools like `git-deploy`_, `fabric`_, or `capistrano`_, can make git+ssh
deployments easier to manage, but there are other ways that make them
even easier.

.. _12factor: http://12factor.net/build-release-run
.. _git-deploy: https://github.com/git-deploy/git-deploy
.. _fabric: http://fabric.rtfd.org
.. _capistrano: http://capistranorb.com/


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

It wasn't until interpreted languages like PHP, Ruby, and Python started
being used primarily for web development, that people shifted towards
git+ssh deployments.

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
something like my `racktables`_ deployment config. A horrible mess of
unpacking a tarball, ensuring the checksum is correct, and extracting
files to the right place.

.. _racktables: https://github.com/osuosl-cookbooks/racktables/blob/v0.3.2/recipes/source.rb

Maybe, just maybe, there's a way we can get there.


Native Packages
--------------

Enter native packages!

Native packages make the ideal world I described a reality. They benefit
both developers and system administrators by allowing the developers to
succinctly define how their application gets setup and torn down, and
relieving system administrators the headache of managing fickle
deployment configuration systems.

There are not extra deployment scripts to manage, and the `12factor`_
pattern of keeping build and deploys separate is maintained.

Hosting an internal package server can also provide the benefit of
mitigating Man-in-the-Middle attacks. Binaries are signed and uploaded
to the package server, and downloaded by the application server.
Signatures are checked by the application server, and invalid signatures
stop malicious code from being installed.


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
