You Should Be Using Native Packages
===================================

As a system administrator and developer, it's my job to write code,
deploy that code, and make sure that code stays running on servers.

Now these two parts of me, are always at odds.

Part of me says "Just ship it!"

.. image:: _static/deployment/shipit.gif
    
While the other screams "It's not perfect yet!"

.. image:: _static/deployment/perfect.gif

Then there is that third morphed version of me that says, "That
deployment is so horrible to maintain!"

.. image:: _static/deployment/unmaintain.gif

Having been a sysadmin for several years, I have learned that deploying
with git is just utterly unmaintainable.


Git
---

Now, also being a developer, I understand where this mindset comes from.
The simplest way to get my application on a server is by using the tools
I'm already familiar with. 

`FTP is so 90's Let's deploy via Git instead!
<https://coderwall.com/p/xczkaq?&p=1&q=>`_ was posted to HN a
while back. 

My response: If "FTP is so 90's", then "Git is so 2000's".

With git there are too many edge cases and problems that arise after the
first deployment. 

    New release? Okay ``git checkout --force``. Huh, files that were ``git
    rm``'ed are still around? Alright ``git clean -xdf``. Wait that just
    wiped out our local config, crap! Okay, let's just run the deploy
    script again.  Wait, that's not the right version. What do you mean
    we *just* released a new version?! GAAHH!!!

Deploying with git also breaks the `12factor`_ pattern for scalable
applications by merging the build and deploy steps.

    "But I *like* how easy my git deploys are! You, you boat rocker!"

If you still feel git and ssh is *the way* to deploy your application,
that's fine, I won't stop you. At least use something like
`git-deploy`_, or wrap things in `fabric`_.


Language Package
----------------

One step up from git+ssh is language specific packaging.

This working for the majority of applications. If, that is, you define
'application' to mean 'library'. 

Using a language specific package manager works for probably 90% of
applications. They provide a single, obvious path to installation, and
with versioning, allow for easy rollbacks.

The problem with language specific packging is that as soon as any
resources are included with the application that aren't written in that
language, things start to break down.

Things like configuration files, assets such as css, html, javascript,
and any external binary (eg. java) that is required for your application
to run.

There are `ways
<https://github.com/pypa/virtualenv/blob/1.11/virtualenv.py#L1987>`_
around this, but they're bad and you generally shouldn't do them.

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

In the real world though, install the package part ends up looking something like this__


A horrible mess of unpacking a tarball, ensuring the checksum is
correct, and extracting files to the right place.

__ https://github.com/osuosl-cookbooks/racktables/blob/v0.3.2/recipes/source.rb

Maybe, just maybe, there's a way we can get there.


Deployment Evolution
--------------------
`Ixiaus <https://news.ycombinator.com/item?id=5930109>`_ provided a
great, sadly minority, response to the HN article

https://hynek.me/articles/python-app-deployment-with-native-packages/




Vision for Socorro
------------------

Currently I'm working on Socorro. It is deployed by pulling down the
deploy.sh script and running it locally on a server. This in turn
creates a local backup, downloads the latests tarball release, ensures
the server is in the correct state (directories, users, permissions,
etc.), and starts the new version.




Notes
=====

Native packages give you all the benefits of git based deploys, coupled
with the shippability of tarballs, the dependency injection of
language specific packages, and security.


They allow you to easily install software, copy over configs, and
rollback to previous versions.




Problems:

* MITM - Someone can install their own version of your software
       - This can happen in multiple places: DNS, Compromised SCM
         server, Language specific package server, Native package server
* Arbitrary Code Execution - Using CI or CD to deploy PRs to staging/dev
  allows people to take over server if you blindly accept all patches
* Secure credentials commited to repo.
* Prod/Stage disparity - First tests of a deploy is on Production

Interpreted Vs. Compiled langagues ==> meaning output is a single binary

scm + ssh
---------

Cons:

* Scalability (Parallel SSH?)

Pros:

* Revisions (SHAs)
* Over encrypted channel (ssh)

Breaks Down:


.. note:: The fact that your configuration is in the same directory as
    your code is a problem, but one I will discuss later.

A lot of time gets spent engineering work arounds for these problems, or
making sure a clean deployment happens. 





tarball
-------

Pros:

* Checksums
* More than just language code

Cons:

* Unsigned
* Scripting/tooling gets pushed to internal code of project, or external
  system like Capestrano, Fabric, etc.

Breaks Down:

Deployments still involve a lot of scripting around extracting, moving,
and copying/updating files. Scripting generally gets pushed into
configuration management or other scripts, not packages with the project
itself.

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
