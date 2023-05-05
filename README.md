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

If you want to read what motivated this, see [The Why](APX-The-Why.md)

1. [Versioning Scheme](#versioning-scheme)
2. [Kernel Package](#kernel-package)
3. [GNU C Library (GLibC)](#gnu-c-library-glibc)
4. [GNU Compiler Collection (GCC)](#gnu-compiler-collection-gcc)
5. [Perl5](#perl5)
6. [Python3](#python3)
7. [Python2](#python2)
8. [TLS Stack](#tls-stack)
9. [Filesystem](#filesystem)
10. [Package Management](#package-management)
11. [Repository Layers](#repository-layers)
12. [JSON Configuration Tool](#json-configuration-tool)


Versioning Scheme
-----------------

YJL will use ‘LTS’ kernels allowing longevity of a release without the
expense of a kernel engineer to back-port kernel patches yet still retain
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


Kernel Package
--------------

YJL will provide vanilla kernel packages (I do not intend to provide
patched kernels) but I also hope to create a system by which a user
can download GPG signed kernel configuration files tailored to their
hardware (say, a particular NUC series) and the GPG signed kernel
source and build customized kernel packages on their system with little
technical experience required.

Kernels will be vanilla LTS kernels and updates will be fron the same
kernel series.

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


GNU Compiler Collection (GCC)
-----------------------------

YJL will use the ‘Current Stable’ branch of GCC when the bootstrap takes
place. Branch release updates of GCC (e.g. GCC 12.2.0 to 12.3.0) will
be made available as updates. Major version updates (e.g. 12.x.y to
13.x.y) would have to take place at the next GLibC bootstrap.

The YJL GCC packaging will always include the c,c++,ada, and d compilers
that are required to build newer versions of themselves. FORTRAN, Go,
Objc/Objc++, and Modula-2 will be made available *except* for in the
`1.core` package repository.


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

GnuTLS is licensed using GPLv3+ and LGPLv2+ which are *without question*
compatible with the licenses of most software on a GNU/Linux system.

GnuTLS will *not* be built with the OpenSSL API compatibility layer.

### LibreSSL

For software (including `kmod`) that needs the OpenSSL API,
[LibreSSL](https://www.libressl.org/) will be used where the OpenSSL
API provided by LibreSSL is sufficient.

LibreSSL will be installed in such a way as to allow a parallel install
of OpenSSL for cases where the OpenSSL API is needed but newer than
the OpenSSL API provided by LibreSSL.

LibreSSL is licensed under the OpenSSL license which is not considered
to be compatible with the GPL licenses however there is a system library
exception.

#### LibreSSL as a System Library

The kernel module loader (kmod) links against LibreSSL, which to me
clearly qualifies LibreSSL as a ‘System Library’ with respect the
[GPL System Library Exception](https://www.gnu.org/licenses/gpl-faq.en.html#SystemLibraryException)
for both GPLv2 and GPLv3.

### OpenSSL

[OpenSSL](https://www.openssl.org/) will be provided for software that
needs the OpenSSL API for which LibreSSL is not sufficient.

OpenSSL is now licensed under the Apache 2.0 license rather than the
OpenSSL/SSLeay license it formerly used.

### FIPS Note

YJL has zero interest in
[FIPS Compliance](https://www.nist.gov/federal-information-processing-standards-fips)

See [LibreSSL Portable Issue 572](https://github.com/libressl/portable/issues/572)

FIPS compliance does not make a system more secure, it only means
there is a means by which to invoke a subset of approved cryptographic
functions that meet a standard defined in a board room, some of which
have not aged very well and should not be used.

If you are obligated to FIPS compliance, use something else, or create
a custom repository with a FIPS-mode OpenSSL and rebuild all TLS related
packages to link against it.


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

See [Repository-Macro](03-Repository-Macro.md) for more information
on how this layering system would work.

Packaging guidelines will need to be written. Some of this has been
started:

* [Non-Standard-Macros](04-Non-Standard-Macros.md)
* [Perl-Modules](05-Perl-Modules.md)
* [APX-RPM-Post-Install-Bug](APX-RPM-Post-Install-Bug.md)


JSON Configuration Tool
-----------------------

This currently is conceptual vaporware without a single line of code
written.

This vaporware tool would be called `json-sysconfig` and would keep
JSON (JavaScript Object Notation) files within the directory
`/var/lib/json-sysconfig`. Either Perl or Python could be used to
write it but I will likely write it in Python (Python3).

Many plain text system configuration files would lend themselves well
to a JSON adaptation and the advantage of a JSON adaptation is that it
would ease interaction of those configuration files with RPM.

As a simple example, the `/etc/shells` file. On a typical minimal system
its contents might look something like this:

    # Begin /etc/shells
    /bin/bash
    /bin/sh
    # End /etc/shells

The sysadmin wants to add the ‘tcsh’ package, some users who come from
a BSD world may feel more comfortable using ‘tcsh’ as their shell, so
when the ‘tcsh’ package is installed it should add both `/usr/bin/tcsh`
and `/usr/bin/csh` to the `/etc/shells` file.

One way to accomplish this is with a generic tool that has specific
configurations and specific code for those configurations.

The tool, say named `/usr/sbin/json-sysconfig`, could take three arguments
when updating its JSON object for the configuration:

1. Keyword for the configuration being managed (e.g. etc-shells)
2. Action to take (e.g. add or remove)
3. Configuration Argument (e.g. `/usr/bin/tcsh`)

The JSON file would correspond with the keyword, for example:

    /var/lib/json-config/etc-shells.json

The ‘tcsh’ package could then have the following scriptlets:

    %post
    if [ $1 == 1 ]; then
    %{_sbindir}/json-sysconfig etc-shells add "/bin/tcsh" ||:
    %{_sbindir}/json-sysconfig etc-shells add "/bin/csh"  ||:
    %{_sbindir}/json-sysconfig etc-shells --update        ||:
    fi

    %postun
    if [ $1 == 0 ]; then
    %{_sbindir}/json-sysconfig etc-shells remove "/bin/tcsh" ||:
    %{_sbindir}/json-sysconfig etc-shells remove "/bin/csh"  ||:
    %{_sbindir}/json-sysconfig etc-shells --update           ||:
    fi

The `json-sysconfig --update` is what would cause the contents of the
JSON object to be written to the corresponding configuration file, but
with a safety precaution.

For every configuration file potentially under the management of the
`json-sysconfig` utility, one entry in the JSON object would be a
SHA-256 checksum.

If either the checksum is

    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

or the checksum matches the *current* configuration file, then the
old configuration (if it exists) is saved as `${filename}.rpmsave-timestamp`
and the new configuration file is written, and the JSON object is
updated with the new checksum.

However for a non-empty file checksum where the checksum in the JSON
database does not match the configuration file to be written, then the
new configuration file is written as `${filename}.rpmnew-timestamp`
leaving the existing configuration file alone, and the JSON object is
updated with the new checksum.

If a system administrator wants to manually maintain a file, editing
the file manually will cause the checksum to no longer match so that
it is never over-written. Alternatively, the system administrator could
simply manually update the checksum to something like

    0000000000000000000000000000000000000000000000000000000000000000

so that it never matches. The command `json-sysconfig --disable etc-shells`
for example could do that automatically.

When a system administrator DOES want the file administered by the
`json-sysconfig` utility again, the system administrator and do something
like:

    json-sysconfig --activate etc-shells
    json-sysconfig --update etc-shells

The `--activate` switch would simply set the checksum to the empty-file
checksum that triggers the utility to re-write the file regardless of
the checksum of the file.

### Kernel Grub Configuration

In theory, such a tool could also be used to manage the `/boot/grub/grub.cfg`
file HOWEVER a separate tool will be written for that for the following
reasons:

1. The `/boot` partition may be shared, so the JSON file would have to
   live on `/boot` instead of within `/var/lib`
2. The management of kernels is more complex, because sometimes the same
   files in `/boot` are under RPM management but also used by multiple
   installs of the operating system.

See [APX-Grub-Configuration](APX-Grub-Configuration.md).


YJL Installer
=============

This is a ways off, but I would like the installer to be ncurses based
(perhaps Python backend, e.g. python dialog) and rather simple.

The disk partitioning tool should be a separate tool from the installer,
for safety I want them separate. I do not want an existing `/boot` or
`/home` to be accidentally formatted, for example.

A separate formatting utility does not guarantee that will not happen
but I suspect it can reduce such mistakes.

The partitioning tool will not *create* volume groups but *probably*
should recognize existing volume groups.

In an age where 256MiB SSDs and 1 TiB platter drives are small, I believe
volume groups are very useful on servers but add un-necessary complexity
to desktop systems—especially when trying to recover data by mounting
a drive on another system.

The partitioning tool will only support the creation of ext2 and ext4
filesystems (er, and swap). Again, this is to ease recovery of data
when necessary.

Nutshell, ext2 will be stronly recommended where journaling is not
needed (for example, `/boot`) and ext4 everywhere else (except for
the swap partition, if created).

In socialist/communal housing (including college dormitories), an
encrypted filesystem can be extremely important for end-users. Support
for encrypted filesystems is planned but will not be available in the
initial release.

If it is possible to *reliably* distinguish between platter drives
and solid state drives, swap partitions would only be permitted on
platter drives and even then, recommended against if the swap partition
is on the same physical drive as the root partition.

I might be convinced otherwise and I still have to research, but I am
under the impression that on single-drive systems and SSD only systems,
a swap file is almost always the better route than a swap partition.

Note that for desktop systems with at least 4 GiB of system memory,
swap is almost never used except when suspending the session (in which
case the entire memory is typically dumped to swap to be reloaded upon
system wake).

A distinct `/boot` partition will *always* be used. It can be shared
with other GNU/Linux installs, but that can be problematic because
some GNU/Linux distributions simply nuke the existing grub configuration
when updating their kernel. I wish that had been something that the
LSB had properly addressed, but it did not. Instead the LSB specified
controversial things like package managers... 🙄

As far as the installer itself is concerned, obviously some hardware
detection has to take place (e.g. network interfaces) but I would like
to keep the installer as KISS as possible.

Perhaps the following installation profiles:

1. Minimal Command Line (repo `1.core.`)
2. Standard Command Line (+ repo `2.cli.`)
3. Xfce Graphical (Standard CLI + repo `3.gui.`, `4.apps.`, `5.xfce.`)
4. MATE Graphical (Standard CLI + repo `3.gui.`, `4.apps.`, `5.mate.`)
5. Xfce + Mate Graphical (Standard CLI + repo `3.gui.`, `4.apps.`, `5.xfce.`, `5.mate`)

Additionally, an option to install the matching "development environment".

Post install, the user can refine their install using DNF (for example,
installing publishing tools like Docbook or an alternate desktop environment
like Gnome3 or Deepin, assuming repositories for them exist).

The ‘Minimal Command Line + Development Environment’ will be all that
is necessary if the user wants a minimal environment with which to build
[Linux From Scratch](https://www.linuxfromscratch.org/) although I do
recommend a desktop environment simply because graphical web browsers
are very beneficial to reading the LFS book.

Not every package that is to be part of YJL will be on the installer.
I want to keep the installer image as small as practical. For those who
need additional packages that are not part of the installer for offline
installation, the relevant package repositories can be downloaded to
physical media via rsync. It may be prudent to once a month or so create
a image that can be written to a thumb drive that contains all of YJL
so that those without an Internet connection or those with slow Internet
can grab it by torrent from somewhere with a good Internet connection
and sneakernet update/install. 
