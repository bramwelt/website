Deployment Strategies
=====================

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

tarball
-------

Pros:

* Checksums
* More than just language code

Cons:

* Unsigned
* Scripting/tooling gets pushed to internal code of project, or external
  system like Capestrano, Fabric, etc.


language package
----------------

Cons:

* Binary files

Pros:

* Only language code. This is never really the case: configs, assets,
  bins, etc.

native package
--------------

Cons:

* Multiple versions of same package (Drupal)

