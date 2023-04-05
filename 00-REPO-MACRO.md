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

These repositories can then have a hierarchal `repo` macro so that as
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

The following list of `%{?repo}` tags is what I plan to use:

1.core
: The core of YJL. Basically LFS plus enough for RPM and basic system
usage including a text browser, mouse support, and cron support.

2.cli
: Programs and libraries that do not need a graphical user interface,
including the rebuild of some packages from the `1.core` repository.

3.gui
: Programs and libraries intended to support a Graphical Desktop
Environment, including the rebuild of some packages from the `1.core`
and `2.cli` repositories.

5.mate
: The MATE Graphical Desktop Environment.

6.xfce
: The XFCE Graphical Desktop Environment.
