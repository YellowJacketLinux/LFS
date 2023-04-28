The %{?repo} Macro
==================

Most (but not all) RPM spec files will have a `Release` tag that contains
the following:

    Release:      %{?repo}N%{?dist}


where `N` is *usually* either a positive integer or is of the form
`0.rcM` or `0.devM` where `M` is a positive integer.

The idea behind this added complexity to the `Release` tag is so that
different repositories can exist that have duplicate packages sometimes
even built from the same RPM spec file but with different capabilities.

These repositories can then have a hierarchical `repo` macro so that as
long as the `Version` is the same, the repository with the greater
`repo` tag will always resolve as the newer package to RPM.

This can help avoid things like GNU Emacs linked against X11 from being
replaced by a GNU Emacs package that is not linked against X11 just
because a “lower-level” package repository rebuilt GNU Emacs with a
larger `N` than the “higher-level” package repository uses.

There are some exceptions, packages that do not have `%{?repo}` in the
`Release` tag. For example, `glibc` and `kernel-api-headers` should
*never* be replaced by packages in a “higher-level” package repository
so those packages simply do not use the `%{?repo}` macro within their
`Release` tag.

Spec files __MUST__ build when the `%{?repo}` macro is not defined, as
it is not a standard RPM macro. When defined, it should be defined by
the build system for the repository, or a user can define it within
their `~/.rpmmacros` file or at package build time.

The `%{?repo}` macro must start with a non-negative integer, followed
by a dot, followed by a code for the package repository.


Planned Package Repositories
----------------------------

The following list of `%{?repo}` tags is what I plan to use. Note that
because the `%{?repo}` tag comes first but may not be defined, it
__MUST__ end in a `.` when it is defined.

___1.core.___  
: The core of YJL. Basically LFS plus enough for RPM and basic system
usage including a text browser, e-mail client, SSH server/client, GPM
mouse support, NTPD client, and fcron support. I likely will add a 
console-based game.

___2.cli.___  
: Programs and libraries that do not need a graphical user interface,
including the rebuild of some packages from the `1.core` repository.

___2.py2.___  
: Python2 and modules for Python2. This repository will not be active
by default.

___3.gui.___  
: Programs and libraries intended to support a Graphical Desktop
Environment, including the rebuild of some packages from the `1.core`
and `2.cli` repositories.

___4.apps.___  
: Graphical programs that require a Graphical Desktop Environment but
are not part of a *specific* Desktop Environment. For example, Firefox
and Thunderbird.

___4.pyworld.___  
: Python 3 modules that are of interest to Python programmers and
students but are not specifically needed by any programs in LFS.

___5.mate.___  
: The MATE Graphical Desktop Environment.

___5.xfce.___  
: The Xfce Graphical Desktop Environment.

It is not a perfect system, but just like taxonomy in biology, I do
not think there ever truly could be a perfect system.

One thing that is specifically part of the design---this system is too
allow third party repositories that want to use YJL as a base but build
package their own way.

For example, my *personal* philosophy is to use GnuTLS as the system
TLS library and use LibreSSL when a TLS software package has not been
ported to GnuTLS---only using OpenSSL when specific library features
of OpenSSL that are not in GnuTLS are needed.

Someone with a different philosophy can simply make a `5.openssl`
repository that replaces packages in YJL with the equivalent versions
but built against OpenSSL. This could be important if, say, FIPS
compliance is mandatory.


Multiple Repository Notes
-------------------------

Some packages may have spec files that can build for multiple package
repositories dependent upon what `%{repo}` evaluates to.

In such cases, the spec file should build for the reasonable default
*without* internally defining the macro.


Spec File ChangeLog Notes
-------------------------

In an RPM Spec File `%changelog` section, both the `%{?repo}` and the
`%{?dist}` tags should be omitted from the `version-release` portion
of the changelog because a package should always be buildable without
those macros defined.
