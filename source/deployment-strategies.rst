You Should Be Using Native Packages
===================================


Seriously, you should.


Here's why.


Native packages give you all the benefits of git based deploys, coupled
with the shippability of tarballs, the dependency injection of
language specific packages, and security.


They allow you to easily install software, copy over configs, and
rollback to previous versions.

A while back I wrote a Chef cookbook for deploying RackTables. I learned
through that process that some web application are just not engineered
to be deployable. During the refactor of that cookbook, I ripped out
everything revolving around extracting the tarball, and turned it into a
simple recipe for managing the RackTables configuration file.

The point is, my configuration for RackTables should have just been::

package 'RackTables' do
  version "0.20.4"
  action :install
end

If only our application deployments could be that simple!

Oh wait...they can, using native packages.





Where I discuss the multiple ways available for deploying web
application, running said code, managing configuration, and their
individual benefits and drawbacks.

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
