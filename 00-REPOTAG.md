The %{?repo} Tag
================

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
