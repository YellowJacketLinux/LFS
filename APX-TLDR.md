TLDR Summary
============

YellowJacket GNU/Linux (YJL) is intended as a hobbyist __DESKTOP__
Linux distribution with releases based on a LTS (Long Term Support)
kernel with rolling updates as the GNU C Library (GLibC) is updated.

New LTS kernels appear *about* once a year, but at least while this
is a small project, new versions of YJL may skip a LTS release or
even two—noting that any hobbyist who needs a newer kernel can always
install a newer kernel without it needing to be an official YJL kernel.

YJL will *never* ship a patched kernel. It is too expensive because
then you have to hire very skilled programmers to deal with bugs and
other issues that the patches may cause. If a hobbyist needs a kernel
feature not in the LTS kernel series YJL ships, YJL includes a C compiler
that allows such a hobbyist to build a newer kernel or patch a kernel
to their hearts content. And I encourage hobbyists to do so, you can
learn a LOT by researching various kernel options.

YJL will not ship an SELinux kernel. SELinux is extremely important for
enterprise Linux, but enterprise Linux specifically is not the goal
and it tends to frustrate desktop users and hobbyists.

For good SELinux distributions, use Debian or RHEL.

New major versions of GLibC tend to appear about every six months.
When a new major version of GLibC does appear, YJL *may* choose to
re-bootstrap against that newer GLibC *however* that is most likely
to happen only when GCC (The GNU Compiler Collection), Perl, and Python
could benefit from updates to the series of those packages that ship
with YJL.

YJL will use SystemD for system services. Note that my current bootstrap
is System V Init but that was a choice mistake that will be fixed before
I have an installer.

YJL is x86-64 with no intentions of porting to other hardware platforms
but who knows about the future.

YJL is __NOT__ multilib but I do have plans to support 32-bit ABI in
`/opt/compat-32` primarily because games but also WINE or whatever, so
in that respect multilib is planned, but as a limited afterthought with
its own toolchain etc.

See [APX-BEYOND-TLDR](APX-BEYOND-TLDR.md) for more thoughts.

