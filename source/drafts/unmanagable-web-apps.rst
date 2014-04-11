Unmanageable Web Apps
=====================

Some web apps just weren't designed to fit into configuration management.
For example: RackTables.

For the last month I have been working on a Chef cookbook to deploy, and
manage RackTables.

---

For the last few weeks I have been learning chefspec, serverspec, and
test-kitchen. I did this at the same time I refactored the first
cookbook I wrote for deploying RackTables.

- Racktables Overview
- Racktables Deployment Methodology (90's PHP)
- Wrangling Racktables into Chef
- The piece of straw: 0.20.4 -> 0.20.7
- Idempotentcy & Web Apps
  - database migrations
  - the need for capistrano/fabric/ssh (reference `aws if ssh failed`
    post)

Overview
--------

Racktables is a MySQL/PHP application for managing server and datacenter
inventory. We use it internally at the OSUOSL because it provides a nice
graphical view of the racks we manage.

Install/Deploy
--------------
This is a quick summary of how to install/deploy Racktables.

Pre-reqs:
 * Apache installed w/php extensions
 * MySQL server w/credentials

Process:
1. Download Tarball
2. Extract to web root.
3. Add vhost to Apache
4. Open browser to application URL
5. Step through install process
6. Write down generated credentials from step #5

Wrangling
---------
Steps 1-3 were easy to get into Chef. Step 5, not so much. This is where
it breaks down.

.. note:: On Generalization - It would be easy for me to say `all web
          apps shouldn't be in CM` but that is a horrendous
          generalization. Web apps are snowflakes, and should be
          treated as such. This is from my personal experience deploying
          RackTables and doesn't apply to every and all web apps.
