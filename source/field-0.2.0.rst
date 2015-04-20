.. _field-0.2.0:

Field - extract fields from a file
==================================

I recently put the final touches on a python project I've been working
on since February, and I am happy to announce the *0.2.0* release of
field!

`field`_ is a command-line application for extracting fields from
files. It was written to be a simpler version of ``awk '{ print COLUMN;
... }'``, and address some of the shortcomings of `cut`_, such as field
ordering, whitespace squashing, and repeated output.

Examples
--------
Extract the user, pid, cpu percent, and command from ``ps``::

    $ ps ux | field 1-3 11 | column -t
    USER      PID   %CPU  COMMAND
    bramwelt  2157  0.0   /usr/bin/gnome-keyring-daemon
    bramwelt  2161  0.0   i3
    bramwelt  2195  0.0   xscreensaver
    bramwelt  2196  0.0   nm-applet
    ...


Extract pid, cpu percent, pid, and command (in that order)::

    $ ps ux | field 2,3,1,11 | column -t
    PID   %CPU  USER      COMMAND
    2157  0.0   bramwelt  /usr/bin/gnome-keyring-daemon
    2161  0.0   bramwelt  i3
    2195  0.0   bramwelt  xscreensaver
    2196  0.0   bramwelt  nm-applet
    ...

Extract user, shell, homedir, uid and gid from ``/etc/passwd`` using *':'*
as the delimiter::

    $ field -f /etc/passwd -d':' 1 7-6 4,3 | column -t
    root    /bin/bash          /root      0      0
    daemon  /usr/sbin/nologin  /usr/sbin  1      1
    bin     /usr/sbin/nologin  /bin       2      2
    sys     /usr/sbin/nologin  /dev       3      3
    sync    /bin/sync          /bin       65534  4
    ...

Further examples can be found in field's manpage.


Download
--------

`field`_ can be installed using pip::

    virtualenv field && source field/bin/activate
    pip install field

For a site-wide install, use::

    sudo pip install field


Contributing
------------

Field is free software and licensed under the GLPv3 (*or later*). The
source can be found on `github`_. If you find any bugs or would like to
suggest improvements, please submit an `issue`_ and I'll do my best to
address it!

.. _cut: https://www.gnu.org/software/coreutils/rejected_requests.html
.. _github: https://github.com/bramwelt/field
.. _issue: https://github.com/bramwelt/field/issues
.. _field: https://pypi.python.org/pypi/field
