Deployable Web Apps
===================

Here is a proposal for deployable web application.

1) Packaged (gem, pip, npm, etc.)
2) Configurable (ini, python, yaml, etc.)

1) install app through package management system
2) run app binary to generate configuration file (templated config
   contained within app.)
3) run app sync database
4) run app database migrations
5) ???
6) App deployed - profit.

7) Everything is in configuration management. Idempotency is central for
   this concept to work.
