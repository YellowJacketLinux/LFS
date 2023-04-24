Packaging of Perl Modules
=========================

This file explains the packaging guidelines that I am attempting to
follow for Free Libre Open Source Software (FLOSS) Perl modules from
[CPAN](https://metacpan.org/)

These guildelines are for RPM packages, not for installing modules via
the native cpan installer (which also works).


YJL RPM Macros for Perl
-----------------------

The RPM Macros used when building Perl and Perl modules are defined
in [`/usr/lib/rpm/macros.d/macros.perl`](SOURCES/rpm-macros-perl-5.36)
which is owned by the `perl-devel` package.

For packaging modules from CPAN, the following macros are used:

* `%{perl5_vendorlib}` --- The base directory for RPM packaged perl
  modules that are architecture independent.
* `%{perl5_vendorarch}` --- The base directory for RPM packaged perl
  modules with compiled components.
* `%{perl5_API}` --- Used in YJL to limit a `noarch` package to the
  series of Perl it was packaged for (e.g. 5.38.x)
* `%{perl5_ABI}` --- Used in YJL to limit a binary package to the
  series of Perl it was packaged for.
* `%{perl5_cpanlic}` --- Used in YJL for the handful of cases where
  a perl packages specifies a license but does not actually include
  the license in the package tarball.

### Spec File Portability Note

The last three listed above should be used in such a way that the spec
file still builds on other systems where they will not be defined.

For the first two listed above, to build a YJL perl module on another
system the user will have to define them on their system. Usually just
adding the following to a `~/.rpmmacros` file will suffice:

    %perl5_vendorlib %{perl_vendorlib}
    %perl5_vendorarch %{perl_vendorarch}

While I could have just used the more standard convention for the
purpose, it is my opinion a good idea to restrict the macros to the
Perl5 just so that it makes it easier to have a future Perl 7 installed
on the same system as Perl 5.

Scripting language specific macros should be versioned, and I chose
to not follow the incorrect mainstream naming scheme just because that
is what all (or most) distributions do.


First Line
----------

The very first line should define the CPAN name of the module in a macro
name `cpanname`. Usually it is the perl module but replacing any
occurrences `::` with a `-`, e.g. the Perl module `Test::More::UTF8`
would have a CPAN name of `Test-More-UTF8`.

Precisely, it has the name of the tarball on CPAN without the version
and tarball extension.

Example first line:

    %global cpanname Text-Template


RPM Spec File Metadata Tags
---------------------------

The RPM spec file `Name:` metadata field then contains the following:

    Name:     perl-%{cpanname}

For the RPM spec file `Summary:` metadata field, it is best to use the
summary provided after the __NAME__ heading on the CPAN web page for
the Perl module. For example:

    Summary:  Expand template text with embedded Perl

When a Perl module only contains text files as opposed to binary files
(this is usually the case), the Perl module package __MUST__ be defined
as a `noarch` package:

    BuildArch:  noarch

While not strictly required, I do like to have an empty line between
that first group of metadata tags and the next group.

For the RPM spec file `Group:` metadata tag, how to categorize groups
in YJL has not yet been determined. Generally for the present I am
just using `Development/Libraries` as such:

    Group:    Development/Libraries

To me that does not quite feel right as most perl modules are both
development *and* runtime libraries. I will figure that out later.
It seems on my CentOS 7.9.2009 (running the ancient Perl 5.16.3)
that many Perl modules just do not specify a group. Anyway...

For the 
