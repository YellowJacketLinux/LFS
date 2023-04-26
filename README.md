YellowJacket GNU/Linux (YJL)
============================

YellowJacket GNU/Linux is currently a *personal* GNU/Linux distribution
that is based upon [Linux From Scratch 11.3](https://www.linuxfromscratch.org/)
built using [CentOS 7.9.2009](https://www.centos.org/) as the build
host.

When an installer is ready, I will welcome contributors to this project
but if it never becomes popular, I will still use and maintain it myself.

The purpose of YJL is to be a desktop distribution for hobbyists.
Commercial ‘Enterprise’ GNU/Linux is of no interest for this project.


Versioning Scheme
-----------------

YJL will use ‘LTS’ kernels allowing longevity of a release without the
expense of a kernel engineer to backport kernel patches yet still retain
a stable kernel API for the release.

Thus, it is logical to me to give a YJL release the same version as the
LTS kernel it ships with.

If I had an installer now, it would thus be:

__Yellow Jacket GNU/Linux 6.1__

to indicate the Linux 6.1 series kernel is shipped with it.

### GLibC Subversion

YJL will have a subversion referencing the version of GLibC used for
the build. The subversion will be referenced in the `/etc/yjl-release`
tag.

If I had an installer now, that file would thus contain:

    Yellow Jacket GNU/Linux 6.1 (GLibC 2.37)

### Kernel Package

YJL will provide vanilla kernel packages (I do not intend to provide
patched kernels) but I also hope to create a system by which a user
can download GPG signed kernel configuration files tailored to their
hardware (say, a particular NUC series) and the GPG kernel source and
build customized kernel packages on their system with little technical
experience required.

### The Philosophy

When a given LTS kernel provides what a user needs, that user should
not have to upgrade their install to a completely new version that may
do things quite differently (like the SystemV to SystemD init upgrade,
X11 to Wayland, etc.) just to have a system that has modern libraries
and programs.

An upgrade of YJL to a newer LTS kernel does not mean there will be
major structural updates to how YJL works, but if there are, that is
when they will happen.

Of course a user can install a newer kernel (even non-LTS) if they so
choose and/or need features of a newer kernel but do not want the
structural changes of a newer YJL.


GNU C Library (GLibC)
---------------------

Every time a new stable version of GLibC is released (about every six
months) another bootstrap of YJL will take place using the new GLibC.

Once all packages are built and a testing period has been performed,
the new subversion will be released as an update to the old previous
subversion thus allowing the update to take place.


GNU C Compiler (GCC)
--------------------

YJL will use the ‘Current Stable’ version of GCC when the bootstrap
takes place. Point release updates of GCC (e.g. GCC 12.2.0 to 12.2.1)
will be made available as updates. Major version updates (e.g. 12.2.x
to 12.3.x) would have to take place at the next GLibC bootstrap.

The YJL GCC packaging will always include the c,c++,ada, and d compilers
that are required to build newer versions of themselves. Fortran, Go,
and Objc/Objc++ will be made available *except* for in the `1.core`
package repository.

Older versions of GCC *may* be made available in `/opt/legacy` but will
only provide c/c++ compilers if made available.


Perl5
-----

YJL will use the ‘Current Stable’ version of Perl5 when the bootstrap
takes place. Point release updates of Perl5 (e.g. 5.36.0 to 5.36.1)
will be made available as updates. Major updates to Perl5 (e.g. 5.36.x
to 5.38.x) would have to take place at the next GLibC bootstrap.


Python3
-------

YJL will use the ‘Current Stable’ version of Python3 when the bootstrap
takes place. Point releases of Python3 (e.g. Python 3.11.2 to 3.11.3)
will be made available as updates. Major updates to Python3 (e.g. 3.11.x
to 3.12.x) would have to take place at the next GLibC bootstrap.


Python2
-------

Python2 is an expired environment but there still are legitimate reasons
to have it for some users.

The last version of Python2, with some security patches, will be available
in an optional add-on repository.

It will install into `/opt/legacy/python2` as the install prefix. Scripts
that call Python2 should call it using the shebang:

    #!/usr/bin/env python2

The user calling it will of course have to have the appropriate path.

Some add-on modules will be built for it as need arises.


TLS Stack
---------

[GnuTLS](https://www.gnutls.org/) will be the default system TLS stack.
Any software that needs a TLS stack that *can* be built against GnuTLS
*will* be built against GnuTLS.

GnuTLS will *not* be built with the OpenSSL API compatibility layer.

### LibreSSL

For software (including `kmod`) that needs the OpenSSL API,
[LibreSSL](https://www.libressl.org/) will be used where the OpenSSL
API provided by LibreSSL is sufficient.

LibreSSL will be installed in such a way as to allow a parallel install
of OpenSSL for cases where the OpenSSL API is needed but newer than
the OpenSSL API provided by LibreSSL.

### OpenSSL

[OpenSSL](https://www.openssl.org/) will be provided for software that
needs the OpenSSL API for which LibreSSL is not sufficient.


Filesystem
----------

YJL will follow the
[FHS 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/index.html)
specification.

Despite being a 64-bit operating system, LFS will use `/{,usr/}lib`
for libraries rather than the `/{,usr/}lib64` that the majority of
64-bit x86\_64 Linux distributions use.

There are plans for multilib support, but done differently than most
distributions do it.

For more information, see [FHS-Note](01-FHS-Note.md) and
[Multilib-Note](02-Multilib-Note.md).


Package Management
------------------

YJL will use the [RPM Package Manager](http://rpm.org/) for package
management.

RPM was chosen because I have a lot of personal experience with it,
not because it is inherently better than other available options.


Repository Layers
-----------------

“Ogres are like onions. Onions have layers. Ogres have have layers.
Onions have layers. You get it? We both have layers.” --- Shrek

Unlike distributions that try to package everything under the sun,
YJL will provide a solid core that groups of users with a particular
interest or need can build on top of---even replacing packages in
the solid core if their specialist need requires it.

See [01-Repository-Macro](01-Repository-Macro.md) for more information
on how this layering system would work.

Packaging guidelines will need to be written. Some of this has been
started:

* [01-Non-Standard-Macros](01-Non-Standard-Macros.md)
* [01-Perl-Modules](01-Perl-Modules.ms)
* [APX-RPM-Post-Install-Bug](APX-RPM-Post-Install-Bug.md)
