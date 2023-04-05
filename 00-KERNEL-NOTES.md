Kernel Notes
============

LFS tends to use the most recent kernel that is tagged “stable” at
[kernel.org](https://kernel.org/) when a development version of LFS
reaches the “Release Candidate” phase. That is a very reasonable
decision and probably the right decision for the LFS book.

My *personal* preference is the use the most recent kernel version
that is tagged “Longterm Maintenance” at
[kernel.org/releases.html](https://www.kernel.org/releases.html).
Sometimes (as was the case with LFS 11.3) those are in fact the same
version but sometimes they are not.

My rationale is that (possibly a result of my autism) I am not always
fond of change forced upon me. That is one of the reasons I preferred
CentOS to Fedora.

With “Longterm Maintenance” kernels, critical bug fixes (primarily
security fixes) are back-ported into the kernel series for many years.

The `6.1` kernel series, for example, will receive these bug fix
back-ports until a projected EOL of December, 2026. Such a long
maintenance period means that for quite some time I am still able to
benefit from the kernel back-ports if I have a system I am not ready to
update, and I like knowing that.

For those who want a newer kernel than “Longterm Maintenance” it is
of course possible to build a newer kernel, but sometimes that does
mean some interfaces change a name or closed source drivers need an
update to properly interface with it.


Kernel Patches
--------------

My preference is to __not__ use kernel patches, but instead build
vanilla kernels.

Some GNU/Linux distributions do include kernel patches bringing in
features that are beneficial to some, but those benefits tend to
matter more for enterprise purposes than for the desktop user.


Current Kernel Spec File
------------------------
The `genesis.N` kernel configuration currently being used has some
Intel Xeon E3 specific kernel optimization options chosen in the
kernel configuration that are not suitable for a generic kernel, and
there are likely a lot of kernel modules many need that are not being
built.

In other words, it is __not__ a suitable kernel configuration for
general use.

The current kernel RPM spec file does not use an initrd and it does
not update the `grub.cfg` file. I do have a plan for how to do that.


Future Plans
------------

When and if I ever get to the point of a working installer, my hope is
to have a generic kernel packaged both with and without an initrd, with
some hardware specific builds available (e.g. specific for Intel NUC)
available either as a kernel package or as a configuration file that
can easily be used by a user to build their own kernel RPMs.

What I mean by the configuration file is a collection of specific kernel
configurations that users can further customize as desired, and have
a simple program that downloads new releases in a kernel series, verifies
the GPG signature, and uses their configuration file to build and install
their own kernel update package.

That however is quite some time away.
