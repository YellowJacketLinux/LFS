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


GNU C Library (GLibC)
---------------------

YJL will use the ‘Current Stable’ version of GLibC when the bootstrap
takes place and will not be updated within a YJL release cycle unless
there is a serious security issue that can not easily be addressed by
patching the YJL GLibC version of GLibC.

Upgrading GLibC is not *supposed* to break binary compatility as long
as the __SAME__ kernel headers are used, and usually it does not break
binary compatibility, but I am convinced it is better to not update
GLibC if and when known security or other critical bugs can patched
within the running version of GLibC.


GNU C Compiler (GCC)
--------------------

YJL will use the ‘Current Stable’ version of GCC when the bootstrap
takes place. Point release updates of GCC (e.g. GCC 12.2.0 to 12.2.1)
will be made available as updates. Major version updates (e.g. 12.2.x
to 12.3.x) *may* be made available as packages that install in `/opt`
in parallel to the system GCC.

The YJL GCC packaging will always include the c,c++,ada, and d compilers
that are required to build newer versions of themselves. Fortran, Go,
and Objc/Objc++ will be made available *except* for in the `1.core`
package repository.

Older versions of GCC *may* be made available in `/opt` but will only
provide c/c++ compilers.


Perl5
-----

YJL will use the ‘Current Stable’ version of Perl5 when the bootstrap
takes place. Point release updates of Perl5 (e.g. 5.36.0 to 5.36.1)
will be made available as updates.

There should only ever be one Perl5 interpreter on a system. When a
Perl series is no longer being updated, YJL *may* provide an *optional*
update repository that allows the system Perl5 to be updated to a
newer series.


Python3
-------

YJL will use the ‘Current Stable’ version of Python3 when the bootstrap
takes place. Point releases of Python3 (e.g. Python 3.11.2 to 3.11.3)
will be made available as updates.

There should only ever be one Python3 interpreter on a system. Due to
the fact that many applications (including RPM itself) build Python
modules of their own that are tied to a Python3 series, it is unlikely
that new Python3 series will be made available when the current Python3
series is no longer receiving updates.


Python2
-------

Python2 is an expired environment but there still are legitimate reasons
to have it for some users.

The last version of Python2, with some security patches, will be available
in an optional add-on repository.

It will install into `/opt/legacy/python2` as the install prefix. Scripts
that call Python2 should call it using the shebang:

    #!/usr/bin/env python2

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

For more information, see [01-FHS-Note](01-FHS-Note.md) and
[01-Multilib](01-Multilib.md).



