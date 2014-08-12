You Should Be Using Native Packages
===================================

As a system administrator and developer, it's my job to write code,
deploy that code, and make sure that code stays running on servers.

Now these two parts of me, and my job, are always at odds.

Part of me says 'Just ship it!'

.. img:: deployment/shipit.gif
    
while the other screams "It's not perfect yet!"

.. img:: deployment/perfect.gif

Then there is that third morhped version of me that says, "That
deployment is so horrible to maintain!"

.. img:: deployment/unmaintain.gif

Ideal World
-----------

My ideal world looks something like this in a Chef resource

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

    service "application" do
        supports :restart => true
        action [:enable, :start]
    end


In the real world though the package part ends up looking something like this__

__ https://github.com/osuosl-cookbooks/racktables/blob/v0.3.2/recipes/source.rb

Maybe, just maybe, there's a way we can get there.

Deployment Maturity
-------------------
Enter Native Packages!

But first, wait, what's wrong with all the others? I *like* how easy my
git deploys are you, you boat rocker!

`Ixiaus <https://news.ycombinator.com/item?id=5930109>`_ provided a
great, sadly minority, response to the HN article on `Let's deploy via Git
<https://coderwall.com/p/xczkaq?&p=1&q=>`_




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
* Building on the server - Only have repo, so any added dependencies
  (packages, binaries, etc) need to be added seperately - 12factor
  lables this build & deploy in one

Pros:

* Revisions (SHAs)
* Over encrypted channel (ssh)

Breaks Down:

New release? Okay 'git checkout --force'. Huh, that thing that we git
rm'ed is still around? Alright 'git clean -xdf'. Wait that just wiped
out our local config, crap gotta run the deploy script again. Deploy.
Wait, that's not the right version. What do you mean we _just_ released
a new one?! GAAHH

.. note:: The fact that your configuration is in the same directory as
    your code is a problem, but one I will discuss later.

A lot of time gets spent engineering work arounds for these problems, or
making sure a clean deployment happens. 

If you still feel git and ssh is *the way* to deploy your application, I
won't stop you. But please, look at things like `git-deploy`_ to manage
it.


language package
----------------

Cons:

* Binary files

Pros:

* Only language code. This is never really the case: configs, assets,
  bins, etc.

Breaks Down:

Non-libraries. Anything that requires files other than pure language
code are not going to work. This doesn't mean test fixtures or other
internal assets, but things like config files, visual assets, different
language binaries, etc.

These can be included with the package, but normally other code will
need to be written to move them somewhere useful like '/usr/share', or
'/etc'.

Some language package manager allow you to do silly things, like upload
the same version of a package. This means when your server tries to
install the package, it sees it already has the right version and
doesn't update it (like it should). It also means you can get different
results from package managers on different systems. Some download
tarballs, some wheels.


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
