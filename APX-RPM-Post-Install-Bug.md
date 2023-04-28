RPM Post Install Bug
====================

Current versions of RPM have a bug related to elf libraries that have
the execution bit set for which RPM does not think the execution bit
needs to be set. An example is with shared libraries.

In older UNIX systems (like HP-UX) shared libraries needed the execution
bit set due to the way the operating system managed them in memory.

For this reason, linkers almost always set the execution bit when
linking shared libraries.

With most (all?) modern UNIX-like operating systems, including GNU/Linux,
shared libraries do not specifically need the execution bit set for them
to remain in memory as usable objects. Modern versions of RPM try to
detect cases where elf objects have the execution bit set but do not
need it set, and automatically removes the execution bit in the post-
install scriptlets that RPM runs after the `%install` part of the spec
file but before it packages the file.

Unfortunately the script responsible for this detection is broken and
it does not properly detect cases where a shared library *genuinely*
needs the execution bit set, such as is the case with `ld-linux-x86-64.so.2`.

The issue is that some shared libraries are in fact executable and
need to be executable so that they can be used as programs.

Bottom line, when a shared library does not need the execution bit set
it does not harm anything to have it set, but when a shared library
DOES need the execution bit, it breaks stuff when it is not set.

In the case of `ld-linux-x86-64.so.2`, the entire operating system
breaks when it does not have the execution bit set!

There are (at least) two solutions to the problem:

1. Disable the scriptlet that removes the execution bit from shared
   libraries and other elf object that are not detected as stand-alone
   executables.
2. Explicitly set the `%attr()` in the `%files` section to be executable,
   as that over-rides the permissions on the file when the package is
   created.

I prefer the second option because it works everywhere, the spec file
will work regardless of whether or not the builder has disabled that
particular scriptlet.

After experience a broken system as a result of that bug, I have started
setting the `%attr()` on most files, libraries or not, just to future-
proof my spec files against similar bugs.

With *almost all* shared libraries I do specify:

    %attr(0755,root,root) %{_libdir}/libfoo.so.X.Y.Z

In most cases, setting `0644` permissions would be fine, but `0755`
on a shared library does not harm anything and avoids me needing to
check each shared library to determine if that particular shared library
is in fact used as a stand-alone executable.

Basically, what the RPM developers did is attempt to solve a problem
that does not exist (executable shared libraries do not harm anything)
and in doing so they created a new problem that did not previously
exist.

The lesson I learned is to manually set file permissions whenever it
is practical---even where RPM does not currently alter it---to avoid
being bitten by this type of bug in the future.

If bored, one can try to execute shared libraries from the command
line. If the result is a segmentation fault, it is *probably* safe to
set `%attr(0644,root,root)` for that particular library, but I am not
that bored.

Anyway, that is why you will see a lot of manually set attributes in
my spec file where it seems they are not actually needed.

