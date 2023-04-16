Non-Standard RPM Macros
=======================

RPM itself defines many macros and there are several other macros that
are non defined by RPM but are considered ‘defacto-standard’ such as
some of the python macros.

When using non-standard macros that are defined outside of an RPM spec
file, the RPM spec file *must* accomodate building when and where that
macro is not defined.

The following non-standard macros are being used by YJL.


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

See the file [00-REPO-MACRO.md](00-REPO-MACRO.md) for more information.

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

An example from the [gcc.spec][SPECS/gcc.spec] file:

    # buildlevel 0 is just c,c++,ada,d -- the languagers
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
