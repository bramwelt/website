How Grub ate my ~.

Recently I installed Windows 8 after my roommate convinced me to play
some PC games with him.

[I don't like windows.] But that's a rant for another time.

At the time I had a 120GB hard drive partitioned in two 60GB sections.
The first was unallocated from the previous time I had been running
windows, and the second was being used for my Debian install.

Well, after I installed Windows 8, I could no longer boot.

This is my explination of why that happens, how I fixed it, and why the
black magic fix works.


Why:
    All operating systems need some section of disk space to boot from.
    This is what '/boot' means. Windows requires the first section of
    the first hard disk. Always. That means Windows always overwrites
    the first 500 bytes of /dev/sda1, no matter what. When you install
    windows it installed the window MBR to the first hard drive. It
    doesn't care what you have there. Your picture you took of your
    family from that vacation last year. Your prized patent that earns
    you millions of dollars. The code that is used by other operating
    systems to boot. It doesn't care. It just overwrites it. Because
    that is the place that it is hard coded to look to boot.

How:
    Boot to a Live CD.
    Download and install grub to the live instance.
    mount your boot partition to /boot
    run grub-install


Black Magic explained:
    grub is a hack that copies your kernel and startup files to a
    specific section of the hard drive, that way when you start up your
    computer it has everything it needs to load up your operating
    system. To do this it needs /boot to exists because that is where it
    looks for those files. It then copies /boot/grub to the specified
    device (you can have your system boot to /dev/sdb) with the <GRUB
    FLAG>.

