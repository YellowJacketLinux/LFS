Non-Standard RPM Macros
=======================

RPM itself defines many macros and there are several other macros that
are non defined by RPM but are considered ‘defacto-standard’ such as
some of the python macros.

When using non-standard macros that are defined outside of an RPM spec
file, the RPM spec file *must* accomodate building when and where that
macro is not defined.

The following non-standard macros are being used by YJL.

1. [The `%dist` macro](#the-dist-macro)
2. [The `%repo` macro](#the-repo-macro)
3. [The `%insinfo` macro](#the-insinfo-macro)
4. [The `%runtests` macro](#the-runtests-macro)
5. [The `%libresslAPI` macro](#the-libresslapi-macro)
6. [The `%cpuoptimize` macro](#the-cpuoptimize-macro)
7. [Perl Specific Macros](#perl-specific-macros)
8. [TODO --- Python Custom Macros](#todo-----python-custom-macros)


The `%dist` macro
-----------------

Most distributions use this so it could be considered a ‘defacto-standard’
but it still is better to not assume it is present.

YJL (and most distributions) use it at the end of the RPM `Release:`
tag definition to give a string identifier of the distribution the RPM
package was built for.

The *only* place this macro should be used is at the end of the `Release:`
tag definition (with one exception) and when defined, it should be be
defined within the distribution specific macro definitions of the RPM
package. It *must* start with a `.` and *must not* end with a `.` or
else the package `Release` metadata will be broken.

When used in an RPM spec file it *must* be of the form `%{?dist}` so
that it expands to a zero-length string if not defined.


The `%repo` macro
-----------------

To the best of my limited knowledge, no other distribution uses this
tag.

YLJ uses it to define which package repository within YJL the package
was built for, and also uses it for conditional features depending
upon which package repository it is being built for.

See the [Repository-Macro](03-Repository-Macro.md) for more information.

It is most commonly used at the beginning of a RPM `Release:` tag
definition and when used in RPM `Release:` tag, it *must* be used at
the very beginning of the `Release:` tag definition.

When defined, it *must* start with a positive integer followed by a
`.` followed by a string that defines the repository the package is
being built for. It *must* end in a `.` or else the package `Release:`
metadata will be broken.

When used within the RPM `Release:` tag definition it *must* be of the
form `%{?repo}` so that it expands to a zero-length string if not
defined.

### Using `%repo` for Condition Features

When the `%repo` macro is used outside of the RPM `Release:` tag, it
*must* also be used inside the `Release:` tag as described above.

When the `%repo` macro is used for conditional building, you *must*
define a spec-file specific macro for the actual condition and set it
to a reasonable default.

Then you can test to see if `%repo` is defined and if defined, use
string comparisons to change your spec file defined conditional macro.

An example from the [gcc.spec](SPECS/gcc.spec) file:

    # buildlevel 0 is just c,c++,ada,d -- the languages
    #  that always should be built because they are required
    #  to build themselves.
    # buildlevel 1 adds fortran,go,objc,obj-c++
    %global buildlevel 1
    %if %{?repo:1}%{!?repo:0}
    %if "%{repo}" == "1.core."
    %global buildlevel 0
    %endif
    %endif

In that example, the `%buildlevel` is the spec-file specific macro and
it defaults to a definition of `1`.

If the `%repo` macro is defined, then it checks to see if it is defined
to the string `1.core.` and if it is defined as such, the `%buildlevel`
macro is redefined to a value of `0`.

By doing this, the spec file remains *mostly portable* to build in a
different GNU/Linux distribution. A user who needs the package in a
distribution that does not provide it can rebuild the source RPM and
may not need to manually edit the spec file at all unless they need
conditionals other than the default.


The `%insinfo` macro
--------------------

Many GNU/Linux distributions have the `install-info` command installed
at either `/sbin/install-info` or at `/usr/sbin/install-info`. I
believe that is wrong because users may have a valid reason to need
the command outside the context of system documentation administration,
but it is what it is.

Unfortunately there does not seem to be a RPM standard macro that
defines the location of the `install-info` command, so to maintain at
least *partial* portability of spec files written for YJL, I created
the `%insinfo` macro that in YJL expands to `/usr/bin/install-info`
and when that macro is used, the spec file *must* have the following
fallback to define it if not defined:

    %if %{!?insinfo:1}%{?insinfo:0}
    %global insinfo /sbin/install-info
    %endif

On YJL the macro is defined so the fall-back is not used, but where
the macro is *not* defined, the fallback then defines `%insinfo` to
`/sbin/install-info` which will at least be correct for *some* systems.

When a package installs `.info` files, the `%insinfo` macro *must* be
used in the `%post` scriptlet to add the info file to the info database
and `%insinfo --delete` *must* be used in the `%preun` scriptlet to
remove the file from the info database *when the package is deleted
and not just being updated*.

The code block above *must* be used to define the `%insinfo` macro on
systems where it is not defined by default.


The `%runtests` macro
---------------------

The test suite in some packages takes a *very long* time to complete.
For such packages, the packager may optionally use the presence of a
defined `%runtests` macro to determine whether or not to actually run
the test suite.

If the `%runtests` macro is set, regardless of what it is set to, then
in spec files with conditional testing any test dependency packages
needed to run the tests (such as DejaGnu or Valgrind) *must*
be triggered as `BuildRequires` and the test suite runs.

On the other hand if `%runtests` is *not* defined, then any `BuildRequires`
that are *only* needed for the test suite should *not* be required and
the test suite does not run.

With most packages, tests are fast enough that they just should always
be run.


The `%libresslAPI` macro
------------------------

Packages the require the OpenSSL API but can build against LibreSSL are
built against LibreSSL *however* to keep the RPM spec file portable to
other GNU/Linux distributions that likely do not have `libressl-devel`.

YJL defines the `%libresslAPI` macro so that during package build time,
the RPM spec file can use it as a boolean (either defined or not) to
determ whether it should build require `libressl-devel` or `openssl-devel`.

Example:

    %if 0%{?libresslAPI:1} == 1
    BuildRequires:  libressl-devel
    %else
    BuildRequires:  openssl-devel
    %endif


The `%cpuoptimize` macro
------------------------

There are some packages that can be optimized for the specific CPU they
are being built for.

In such cases, the default build of the package *must* be without the
optimization so that the package will run regardless of the CPU specific
capabilities.

However the user should have the ability to rebuild the source RPM and
benefit from those optimizations if they so choose.

In YJL this is accomplished with the `%cpuoptimize` macro.

### The `Release:` metadata tag

When a spec file offers CPU specific optimization, the RPM `Release:`
metadata tag *must* have `%{?cpuoptimize}` at the *very end* of the
tag *directly after* the `%{?dist}` tag.

If the `%cpuoptimize` macro is not defined, then `%{?cpuoptimize}`
will expand to a zero-length string. When it is defined then the RPM
package name itself indicates it is a CPU optimized package that should
only be installed on that a CPU with the specific capabilities the
build is optimized for.

As the `%cpuoptimize` macro is used at the end of the `Release:` tag,
when defined it *must* begin with a `.` and *must not* end with a `.`
or the `Release:` metadata will be broken.

### Package Build Optimization

In cases where the RPM spec file has to take specific action to build
a generic package, use the following:

    %if 0%{!?cpuoptimize:1} == 1
    [do stuff]
    %endif

An example of that scenario can be seen in the [gmp.spec](SPECS/gmp.spec]
file, where the action takes place during `%setup`.

In cases where the RPM spec file has to take specific action to build
an optimized package, use the following:

    %if 0%{?cpuoptimize:1} == 1
    [do stuff]
    %endif

### Defing the `%cpuoptimize` macro

For packages like GMP where the build script itself determines the
proper optimizations to make, it does not really matter what the macro
is defined to be as long as it begins with a `.`, does not end with a
`.`, and otherwise only contains characters legal in an RPM `Realease:`
metadata tag.

Currently in my `~/.rpmmacros` file I have the following:

    %cpuoptimize .xeonE3

However there may be optimizations where the build scripts (e.g.
`configure`) has to be specifically told what optimizations to make.

It may be necessary to develop a standard list of valid `%cpuoptimize`
definitions to deal with cases where the build scripts have to be told
how to optimize the package.

At present, there are no plans to distribute CPU optimized packages.
I do however desire to make it easy for the user to just rebuild a
source package and get such optimization.

### CPU Optimized Kernel

Linux kernel optimization is not done within the RPM spec file itself
but is performed during `make config`. Kernel packages should not use
this macro tag.


Perl Specific Macros
--------------------

For Perl, see [Perl Modules](05-Perl-Modules.md)


TODO --- Python Custom Macros
-----------------------------

Will add when I upload the `python3.spec` and `python2.spec` RPM spec
files.
