What I Learned Setting Up AutoFS

This last week was spent trying to get autofs setup on Debian 7
(Wheezy). At the OSUOSL we have a shared workstation setup, which
requires LDAP accounts, and NFS mounted home directories. The goal was
to get autofs setup to automount the nfs home directories when user’s
log in. Through the process we determined a nice to have feature was
only the current user’s home dir being mounted, not the entire
collection of home dirs.

Problems we ran into:

* autofs files should not be executable
    - This was not an easily determinable bug, as it resulted in a ‘syntax
      error’ on the implicit autofs map. Usually giving ‘syntax error near [
      WHOLE FREAKIN MAP ]’ which was not helpful.
    - It was resolved through Jordan’s previous knowledge, perhaps his reading
      of man pages.
    - It showed up as a regression later on, due to chef runs

* Always disable configuration management when initially setting up a system
    - Currently I still can’t login to the box because `PermitRootLogin no` is
      set in the sshd_config.
    - Changing the autofs files to not be executable later got switched back
      to executable because of the chef recipes.
    - auto.master was overwritten while debugging, removing the ‘/home’ map
      needed to mount home dirs.

* When working with autofs remove any related mount entries in `/etc/fstab`
    - Jordan thought he had solved the problem, yet it was masked by the fact that the mount was still listed in fstab

* Ignore /etc/auto.master.d/
    - Moving the home map under this may still work, but initially it
      added too much indirection and confusion.
    - It is not clear if the filename of the map is the mount point.

* Double Check mount syntax
    - Multiple times I forgot the ‘-’ at the beginning of options. Which
      led to a much longer time spent debugging and flipping between
      different problems.

* AutoFS docs could be better. The man page even states this!
    - Describe right away the difference between ‘implicit’ and
      ‘explicit’ mappings.
    - Define ‘mapping’ or ‘map’ as it is not listed
    - Provide better examples
    - List defaults (-fstype=nfs) not required, because everything is
      assumed to be nfs if it is omitted.
    - Explain LDAP != user permission, but mount management

* There is a seperate XML file for ldap auth things. This makes no sense
  as there are already options _within_ the config file (one being the
  path to this file) for LDAP.

* LDAP does not mean users
    - Jordan said that LDAP was needed and I went back and forth on this point.
    - I knew LDAP was separate from the mount point, but still needed by
      the box to set the correct user permissions
    - LDAP & AutoFS allows you to setup mountpoint through LDAP and have
      autofs pull them in. Its basically managing autofs within LDAP,
      which...is really wierd. Don’t do that.

* /etc/nsswitch.conf
    - Not required unless using LDAP as mentioned above
    - ‘automount:’ directive documented in autofs, not nsswitch manpages

* +auto.master
    - Not sure what this means still. Is is required? Does it make some
      sort of recursion happen?
    - /home /etc/auto.home - Not sure if it needs to come before or
      after +auto.master line.

* wildcard
    - This is a really cool way to mount subdirectories.
    - \*-mount,options server:/remote/dir/&

Conclusions
Disable CM when setting up a server. Edit -> Test -> Ensure -> Configure
