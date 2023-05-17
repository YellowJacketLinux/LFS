Beyond the TLDR
===============


HARDWARE GOALS
--------------

It is not possible to test YJL with all possible hardware combinations
but I do want to do extensive testing with a particular subset.

One thing I hope to do is make sure any released YJL work on the Intel
NUC platform out of the box going back at least five generations of NUC.
At the time of writing, it looks like Intel NUC 13 is current so a YJL
release today I would *hope* to have *just work* on the NUC 9–13.

That goal may not always achievable, and note that if that goal is
achieved it will *probably* work on earlier and often later as well,
until later gets to the point where new kernel drivers are needed.

The NUC is a very affordable PC often available as an inexpensive kit
without an operating system, especially ‘Old Stock’ when newer versions
of the NUC are released.

For technically minded students from an economically oppressed background,
a NUC is often a very good way for such students to be able to explore
their technical aptitude and learn how to master the technical world.

Of course if such students can get a laptop or desktop I want YJL to
work there too, but when finances are blocker, a NUC despite its hardware
limitations can be a godsend.

For the most part, supporting a NUC just means making sure all the right
kernel modules are built for the hardware and that should not be too
difficult to do, but it also means testing and possibly looking into
making sure the correct software is available (and working) to deal with
the issue of over-heating which is more likely in a NUC *especially* in
houses that may not be able to afford suitable air conditioning.

Sometimes for optimal performance, firmware that is not part of the
Linux kernel firmware distribution is necessary. It *appears* that
Intel is pretty good at making sure their firmware is made available
in that firmware distribution but there may be cases where extra
attention and action is needed.

Basically I hope to be able to aquire Intel NUCs for the purpose of
testing the install and benchmarking the performance and looking into
how to tune what can be tuned for the NUC.

Knock-off NUCs too but at least initially I will have to limit it to
testing/tuning Intel and hope it works properly for the knock-offs as
a side-effect.


Automated Restore Profile
-------------------------

Inspired by the NUC but useful to almost all hardware scenarios, on a
NUC it likely will be somewhat common for `/home` to be on a separate
external USB hard drive. It is also possible that `/home` will reside
on a NAS although support for that *probably* will not initially exist.

I would like to have a directory within `/home` possibly called

    /home/_restore

with `0750,root,root` permissions that includes most metadata needed
to do a quick install of a fresh operating system while retaining
stuff like `/etc/passwd`, `/etc/group`, timezone information, package
information, stuff like that so that when a NUC (or other) PC needs
to be replaced the install can go quickly with very little needed
post-install to bring the system back to where it was before a fresh
install was necessary.



