Packaging of Perl Modules
=========================

This file explains the packaging guidelines that I am attempting to
follow for Free Libre Open Source Software (FLOSS) Perl modules from
[CPAN](https://metacpan.org/)

These guidelines are for RPM packages, not for installing modules via
the native CPAN installer (which also works).


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
  a Perl packages specifies a license but does not actually include
  the license in the package tarball.

### Non-Perl Specific Macros

Virtually every Perl module has tests that should be run, but to avoid
circular dependency issues one should *always* be able to build a Perl
module without running the tests.

The `%{runtests}` macro is a Boolean macro that YJL uses to determine
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

Other distributions LOVE to have distribution-specific Perl and Python
macros that are difficult to identify what it is they are trying to do,
making building their RPM spec files a nightmare on another system, so
I do not feel bad about this deviation one bit *especially* since this
deviation from common practice is cake to work around.


First Line Of The RPM Spec File
-------------------------------

The very first line should define the CPAN name of the module in a macro
name `cpanname`. Usually it is the Perl module but replacing any
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

To me that does not quite feel right as most Perl modules are both
development *and* run-time libraries. I will figure that out later.
It seems on my CentOS 7.9.2009 (running the ancient Perl 5.16.3)
that many Perl modules just do not specify a group. Anyway...

For the RPM spec file `License:` metadata tag, the
[SPDX License Identifier](https://spdx.org/licenses/) should be used.

Many (but not) Perl modules on CPAN specify they use the same license
as Perl5 itself, and on CPAN those packages are labeled as

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
that people trying to build the package for another distribution (such
as CentOS 7 where it is only at version 6.68 if not updated).

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
system regardless of whether or not tests are run.

Some (but not all) binary Perl modules will need a `BuildRequires:`
added for a library dependency, e.g. for XML::Parser which links
against `libexpat.so`:

    BuildRequires:  expat-devel

### Conditional Test Requirements

To run tests, the RPM build system will usually need quite a few additional
Perl modules available---modules used by the test scripts themselves.

Those `BuildRequires:` meta tags should be wrapped inside a conditional:

    %if 0%{?runtests:1} == 1
    BuildRequires:  perl(Foo::Bar) >= 3.14159
    [...]
    %endif

That way, the RPM build system only needs to install them if the `%{runtests}`
macro is defined so that circular dependencies where A requires B for tests,
B requires C for tests, and C requires A for tests can be worked around by
building them without running tests first.

Again in the `"prereqs"` entry of the JSON file, there will be a `"runtime"`
and a `"test"` entry. Everything in there (except for the specified minimum
version of `perl`) should be added within the `%{runtests}` conditional. For
example:

    "prereqs" : {
      [...]
      "runtime" : {
        "requires" : {
          "Carp" : "0",
          "Data::Section" : "0",
          "File::Spec" : "0",
          "IO::Dir" : "0",
          "Module::Load" : "0",
          "Text::Template" : "0",
          "parent" : "0",
          "perl" : "5.006",
          "strict" : "0",
          "utf8" : "0",
          "warnings" : "0"
        }
      },
      "test" : {
        "recommends" : {
          "CPAN::Meta" : "2.120900"
        },
        "requires" : {
          "ExtUtils::MakeMaker" : "0",
          "File::Spec" : "0",
          "Test::More" : "0.96",
          "Try::Tiny" : "0"
        }
      }
    },

would translate to:

    %if 0%{?runtests:1} == 1
    BuildRequires:  perl(Carp)
    BuildRequires:  perl(Data::Section)
    BuildRequires:  perl(File::Spec)
    BuildRequires:  perl(IO::Dir)
    BuildRequires:  perl(Module::Load)
    BuildRequires:  perl(Text::Template)
    BuildRequires:  perl(parent)
    BuildRequires:  perl(strict)
    BuildRequires:  perl(utf8)
    BuildRequires:  perl(warnings)
    BuildRequires:  perl(CPAN::Meta) >= 2.120900
    BuildRequires:  perl(Test::More) >= 0.96
    BuildRequires:  perl(Try::Tiny)
    %endif

Note that I left out `"perl" : "5.006"`, `"ExtUtils::MakeMaker" : "0"`,
and the second `"File::Spec" : "0"`.

Requiring specific versions of Perl itself is problematic because of
`Epoch:` metadata tags that were necessary due to RPM evaluating version
strings as integers delimited by a `.` while Perl evaluated everything
after the dot as fractional.

There is already a `BuildRequires:  perl(ExtUtils::MakeMaker)` that
precedes the `%{runtests}` conditional, so a second is not needed. And
obviously do not also need two `BuildRequires:  perl(File::Spec)` tags.


Run-Time Requirements
---------------------

For the RPM spec file `Requires:` tags, RPM is actually pretty good at
figuring that out automatically *however* I always set it up manually
anyway.

Use the `"runtime"` section of the `"prereqs"` from the `META.json` or
`MYMETA.json` file. For example:


    "prereqs" : {
      [...]
      "runtime" : {
        "requires" : {
          "Carp" : "0",
          "Data::Section" : "0",
          "File::Spec" : "0",
          "IO::Dir" : "0",
          "Module::Load" : "0",
          "Text::Template" : "0",
          "parent" : "0",
          "perl" : "5.006",
          "strict" : "0",
          "utf8" : "0",
          "warnings" : "0"
        }
      },
    },

That translates to:

    Requires: perl(Carp)
    Requires: perl(Data::Section)
    Requires: perl(File::Spec)
    Requires: perl(IO::Dir)
    Requires: perl(Module::Load)
    Requires: perl(Text::Template)
    Requires: perl(parent)
    Requires: perl(strict)
    Requires: perl(utf8)
    Requires: perl(warnings)

Notice again I left out the explicit Perl version requirement. An RPM
package archive restricts the building of the module to a specific series
of Perl versions (e.g. 5.36.x) or on some distributions, an even more
specific of Perl.

For YJL, this is handled with the `%{perl5_API}` and `%{perl5_ABI}`
RPM macros, but they should be used in such a way that the package
still works when built for another distribution.

For `noarch` packages, use the following:

    %if 0%{?perl5_API:1} == 1
    Requires: %{perl5_API}
    %endif

For binary packages, instead use the following:

    %if 0%{?perl5_ABI:1} == 1
    Requires: %{perl5_ABI}
    %endif

In both cases, those `Requires:` are provided by the YJL build of Perl
(see [perl.spec](SPECS/perl.spec)).

By wrapping the `Requires:` in a conditional, the spec files will still
build installable packages on other GNU/Linux distributions as well.


The RPM Package Description
---------------------------

For the `%description` part of a CPAN Perl Module, when available I
just take the description offered on CPAN. Sometimes it does require
some redaction for the purpose of a an RPM package.


The RPM Spec File Build Preparation Section
-------------------------------------------

Generally this will just be the two lines:

    %prep
    %setup -n %{cpanname}-%{version}

In once case, the `Changes` file which I like to package with the
`%doc` macro had an execution bit set on it in the source package.

In that case, I fixed it within `%prep`:

    %prep
    %setup -n %{cpanname}-%{version}
    chmod -x Changes

(using `%__chmod` would have been better, note to self)


The RPM Spec File Build Section
-------------------------------

Most (but not all) Perl modules on CPAN build using a `Makefile.PL`
file to generate the Makefile.

There are other build systems. I will cross that bridge when I come
to them and describe them here, so they can be water under the bridge.

### Makefile.PL Build System

When a Perl module has a `Makefile.PL` the `%build` section should
*almost always* look like this:

    %build
    %__perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
    make %{?_smp_mflags}

The `INSTALLDIRS=vendor` tells `Makefile.PL` that this is being packaged
for installation and should use the directories defined when `%__perl`
was built for distribution vendor-provided Perl modules.

The `NO_PACKLIST=1` tells the `Makefile.PL` not to create a packlist.
A packlist interferes with RPM package installation and the functionality
is provided by RPM itself.

The `NO_PERLLOCAL=1` tells the `Makefile.PL` that `perllocal.pod` should
not be updated. That is for packages installed through the CPAN utility
itself (or manually built on the system).

The `OPTIMIZE="$RPM_OPT_FLAGS"` is really only needed for binary Perl
modules but it does not hurt anything when used with `noarch` Perl
modules. It allows the optimization flags set by RPM to be used. This
is important for binary modules as it includes things like
`-D_FORTIFY_SOURCE=2` that help protect against things like buffer
overflows from being exploited.

With the `make` command, the `%{?_smp_mflags}` again is really only
needed for binary Perl modules but does not hurt anything with `noarch`
Perl modules. It just speeds up the build process on systems that have
more than one CPU core available for building.

### Note on SMP MFLAGS

The value of `%{?_smp_mflags}` is initially defined by RPM based upon
how many cores are available on the system.

My particular hardware uses a case with less than optimal air flow, and
is located in the naturally warmest room of the house.

As a result, when I allow all eight cores to be used and build something
very CPU intensive for long periods of time (like building GCC), on hot
days I actually CPU temperature warnings.

So in my `~/.rpmmacros` file I set the following:

    %_smp_mflags -j4

When only using four cores, the build takes a little longer but I am
less likely to get the CPU temperature warnings and when I do still
get them I can just take the case lid off during the build.

My case is a low-profile 'Media PC' case but with a server motherboard
and a Xeon processor. Furthermore there is a fan-less nVidia GPU in it
with a large heat sink that restricts airflow inside the case.
What I need to do is have a machinist drill ventilation holes in the
lid right above the CPU cooler fan.

Anyway I mention manually setting the `%_smp_mflags` to only use a
subset of available cores in case anyone else has a similar situation
when the default value of ALL cores is used and CPU temperature warnings
happen with very intensive builds.


The RPM Spec File Check Section
-------------------------------

In almost all cases, the `%check` section of the RPM spec file should
look like this:

    %check
    %if 0%{?runtests:1} == 1
    make test > %{name}-make.test.log 2>&1
    %else
    echo "make test not run during package build." > %{name}-make.test.log
    %endif

The `%if` block only runs the test if the RPM build system has defined
the `%{runtests}` macro.

The `%else` block indicates that tests were not run when that macro has
not been defined on the build system.

YJL policy is to log test results and package them with `%doc` just in
case the end user ever wants or needs to review them, so that is why
it is important to indicate tests were not run when they are not run.

On the production build server they will always be run but to package
the results of tests with `%doc` the results file needs to exist even
if the tests were not run.

In some cases, such as when an X11 server is needed to run the tests,
the above `%check` system may need modification.


The RPM Spec File Install Section
---------------------------------

Both `noarch` and binary Perl modules generally need the following
`%install` section:

    %install
    make install DESTDIR=%{buildroot}

Perl tends to install modules without the write bit set. for noarch
packages that is not a problem, but for binary Perl modules it interferes
with the ability for RPM to strip the binaries.

Binary Perl modules thus need the following addition:

    %{_fixperms} %{buildroot}%{perl5_vendorarch}

That will set the write bit so that RPM stripping works.


The RPM Spec File Files Section
-------------------------------

The `%files` should always set the `%defattr`:

%files
%defattr(-,root,root,-)

The package should own all directories it installs inside of the
`%{perl5_vendorlib}` (for noarch) or `%{perl5_vendorlib}` (for binary)
directories, even if those directories are already owned by a module
that is dependency.

With a dependency, it is all possible the dependency is installed in
either `%perl5_privlib` or `%perl5_sitelib` for `noarch` dependencies,
or in `%perl5_archlib` or `%perl5_sitearch` for binary dependencies.

In those cases, the Perl module being packages would leave empty
directories behind when uninstalled if it does own all directories
inside of its module install directory.

Since Perl likes to install without the write bit, I like to manually
specify the attributes of installed files without the write bit.

Due to a bug in current versions of RPM (see (00-RPM-POST-INSTALL-BUG.md))
the attributes of binary modules should set manually anyway.

Honestly the RPM bug may not matter for binary Perl modules, they may
not need the execution bit set to work on GNU/Linux, I do not know.

Anyway what I do is manually set the the attributes for text files
inside the Perl module directory to `0444` and I manually set the
attributes for binary files inside the Perl module directory to
`0555`. Thus, the attributes match what they looked like after the
install but before `%{_fixperms}` and before the RPM scriptlets that
automatically run after `%install`.

Example:

    %files
    %defattr(-,root,root,-)
    %dir %{perl5_vendorarch}/XML
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser.pm
    %dir %{perl5_vendorarch}/XML/Parser
    %dir %{perl5_vendorarch}/XML/Parser/Encodings
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/Japanese_Encodings.msg
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/README
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/*.enc
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Expat.pm
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/LWPExternEnt.pl
    %dir %{perl5_vendorarch}/XML/Parser/Style
    %attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Style/*.pm
    %dir %{perl5_vendorarch}/auto/XML
    %dir %{perl5_vendorarch}/auto/XML/Parser
    %dir %{perl5_vendorarch}/auto/XML/Parser/Expat
    %attr(0555,root,root) %{perl5_vendorarch}/auto/XML/Parser/Expat/Expat.so

### Man Pages

For man pages, the standard `0644` permissions are fine:

    %attr(0644,root,root) %{_mandir}/man3/*.3*

### Make test log

The output of `make test` should be packaged as documentation:

    %doc %{name}-make.test.log

### Package Documentation

Any documentation file within the Perl module source that is potentially
useful to the end user should be packaged with the `%doc` macro.

This usually includes the `Changes` file, a `README` file, any license
files, and with some packages the `examples` directory.


RPM Packaging of the License File(s)
------------------------------------

Note that specification of `%license` is part of the `%files` section.

Every Perl module __MUST__ package the upstream-provided License file(s)
using both the `%license` macro *and* the `%doc` macro.

Furthermore, the packager __MUST__ ensure that the `License:` meta-tag
matches the upstream-provided License file(s).

Unfortunately, a small handful of Perl modules on CPAN do not include
the applicable license files.

It is probably illegal and certainly bad form for anyone other that the
upstream maintainer to add a license file to a package.

For YJL there is a workaround. YJL has a packaged called
`common-CPAN-licenses` that contains *most* of the various Open Source
licenses used in Perl modules on CPAN.

When a Perl module does not include the license text *and* the text
of the licenses specified by the package are included in that package,
add the following to the Run-Time `Requires:` RPM spec file meta tags:

    %if 0%{?perl5_cpanlic:1} == 1
    Requires: common-CPAN-licenses
    %endif

Then in the spec file `%install` section, add something like the
following:

    %if 0%{?perl5_cpanlic:1} == 1
    cat > Perl5-Licenses.txt << "EOF"
    This package specifies it uses the Perl 5 licenses but did not include
    them in the package source.

    They can be found in the following directory:

      %{perl5_cpanlic}/Perl5/

    EOF
    %endif

Obviously if the package does not specify the Perl 5 license, then that
needs to be tailored to the license it does specify.

The created `Perl5-Licenses.txt` (or whatever if it is a different
specified license) can then be conditionally included in `%files`:

    %if 0%{?perl5_cpanlic:1} == 1
    %license Perl5-Licenses.txt
    %doc Changes README samples Perl5-Licenses.txt
    %else
    %doc Changes README samples
    %endif
    %doc %{name}-make.test.log


End Notes
---------

These are general guidelines. There are conditions that are not covered
by these guidelines, and conditions that may require deviation from them.











