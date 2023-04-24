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

### Non-Perl Specific Macros

Virtually every Perl module has tests that should be run, but to avoid
circular dependency issues one should *always* be able to build a Perl
module without running the tests.

The `%{runtests}` macro is a boolean macro that YJL uses to determine
whether or not tests should be run.

To conditionally run tests, I use the following in my `~/.rpmmacros`
file:

    %runtests fubar

When I do not wish to run tests, I just comment that out my
`~/.rpmmacros` file.

More information on that macro can be found at
(00-NON-STANDARD-MACROS.md#the-runtests-macro)

The `%{_fixperms}` macro is a standard RPM macro that expands to
`/usr/bin/chmod -Rf a+rX,u+w,g-w,o-w`

Perl likes to install stuff without the write permission bit set, and
that causes problems when RPM wants to strip a binary library.

That macro is only needed for binary modules and is a standard part of
RPM itself.

### Spec File Portability Note

Of the five YJL Perl specific RPM macros, `%{perl5_API}`, `%{perl5_ABI}`,
and `%{perl5_cpanlic}` should be used in such a way that the spec file
still builds on other systems where they will not be defined.

For `%{perl5_vendorlib}` and `%{perl5_vendorlib}`, to build a YJL Perl
module RPM spec file on another system the user will have to define those
macros on their system. Usually just adding the following to a
`~/.rpmmacros` file will suffice:

    %perl5_vendorlib %{perl_vendorlib}
    %perl5_vendorarch %{perl_vendorarch}

While I could have just used the more standard convention for the
purpose, it is my opinion a good idea to restrict the macros to the
Perl5 just so that it makes it easier to have a future Perl 7 installed
on the same system as Perl 5.

Scripting language specific macros should be versioned, and I chose
to not follow the incorrect mainstream naming scheme just because that
is what all (or most) distributions do.

Other distros LOVE to have distro-specific Perl and Python macros that
are difficult to identify what it is they are trying to do, making
building their RPM spec files a nightmare on another system, so I
do not feel bad about this deviation one bit *especially* since this
deviation from common practice is cake to work around.


First Line Of The RPM Spec File
-------------------------------

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

For the RPM spec file `License:` metadata tag, the
[SPDX License Identifier](https://spdx.org/licenses/) should be used.

Many (but not) Perl modules on CPAN specify they use the same license
as Perl5 itself, and on CPAN those packages are labelled as

    License: perl_5

Perl 5 is dual-license, giving the user the option of using either the
GPL 1.0 (or newer) or the Perl Artistic license.

The correct way using SPDX to specify the `License:` metadata tag in
those cases:

    License:  GPL-1.0-or-later or Artistic-1.0-Perl

For the RPM spec file `URL:` metadata tag, it should point to the URL
on CPAN for the module. For example:

    URL:      https://metacpan.org/pod/Text::Template

The RPM spec file `SOURCE:` metadata tag needs to point to the CPAN
link for the module source tarball:

    Source0:  https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/%{cpanname}-%{version}.tar.gz

The path on `cpan.metacpan.org` will differ according to the author of
the package.


BuildRequires
-------------

Every Perl module needs

    BuildRequires:  perl-devel

That is the package that owns the file defining the Perl specific RPM
macros that are used when building a Perl module.

Any package that builds using `Makefile.PL` (most of them) will need

    BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76

The reason for that, some of the options that are passed to `Makefile.PL`
are not defined in earlier versions of `ExtUtils::MakeMaker`.

Of course if the package itself specifies an even newer version of
`ExtUtils::MakeMaker` is needed, then specify the newer version.

Note the version of `ExtUtils::MakeMaker` in Perl 5.36.1 is 7.64, for
YJL itself that version requirement will always be met regardless of
whether or not it is specified, but it still needs to be specified so
that people trying to build the package for another distro (such as
CentOS 7 where it is only at version 6.68 if not updated).

### Determining Build Requirements

For other build requirements, a packager needs to distinguish between
those that are actually needed to build the module and those that are
only needed if running tests.

For `noarch` Perl modules that make use of `Makefile.PL`, usually
`perl-devel` and `perl(ExtUtils::MakeMaker) >= 6.76` are the only
`BuildRequires` needed outside of the test suite.

Inside the module source, there will be a file usually called `META.json`
or `MYMETA.json` that can be used to find out the proper build
requirements.

There will be a JSON entry called `"prereqs"` that has the information
needed.

Within that entry, ignore what it is `"develop"` but generally anything
that is `"configure"` should be added as a RPM spec `BuildRequires:`
meta tag, wrapped of course in `perl()`. For example:

    "prereqs" : {
      "configure" : {
        "requires" : {
          "ExtUtils::MakeMaker" : "6.78"
         },
        "suggests" : {
          "JSON::PP" : "2.27300"
        }
      },
      [...]
    },

That would translate to:

    BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
    BuildRequires:  perl(JSON::PP) >= 2.27300

Note that in that example, `perl(JSON::PP) >= 2.27300` is not *strictly*
required to build it as it is only listed as `"suggests"` but with a
few exception, I do `BuildRequires:` the `"suggests"`.

Those are the `BuildRequires:` that *must* be present on the RPM build
system regardless of whether or not tests are run,








