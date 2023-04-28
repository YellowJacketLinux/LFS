Filesystem Hierarchy Standard Note
==================================

In the FHS, `/{,s}bin` *may* be a symlink to `/usr/{,s}bin` and
`/lib{,64}` *may* be a symlink to `/usr/lib{,64}`.

Many modern Linux distributions do in fact implement those directories
as symbolic links.

For an RPM `.spec` file to truly be portable, it can not assume that
those directories are symbolic links and binaries/libraries that belong
within `/bin`, `/sbin`, `/lib`, and `/lib64` when they are not symbolic
links should be installed in those directories and not under the `/usr`
prefix.

For binaries within `/{,s}bin`, any shared libraries they link against
*must* be installed within `/lib{,64}` so that the binary will work in
the event `/usr` is a separate partition that is not mounted.

Shared Library Packaging
------------------------

For the shared libraries installed within `/lib`, I am choosing to put
the developer `libfoo.so` symbolic link and (if packaged) the developer
`libfoo.a` static library within `/usr/lib` even though the shared
library itself is within `/lib` and not under the `/usr` prefix. Those
files are not needed in the event `/usr` is not available.

With a very few exceptions (e.g. `libgcc_s` and `libstdc++` from `gcc`)
the way I do this is to pass

    --libdir=/%{_lib}

to the configure script.

That does result in the shared library being placed within `/lib`
but *usually* it also results in the `pkgconfig` directory also being
placed in `/lib` along with `foolib.so` and (if built) `foolib.a`.
Furthermore, the `foolib.pc` points to `/lib` for linking, which
technically is correct if that is where the `foolib.so` and `foolib.a`
files are located. However I do not want them in `/lib`.

In a *very few* cases, the resulting `Makefile` is smart enough to do
what I want (put `foolib.so` in `/usr/lib` and `foo.pc` in
`/usr/lib/pkgconfig` correctly configured) but usually I do have to
manually adjust the install.

An example from the `zlib.spec` file:

    install -m755 -d %{buildroot}%{_libdir}
    sed -i 's?libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/zlib.pc
    mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/
    rm -f %{buildroot}/%{_lib}/libz.so
    ln -s ../../%{_lib}/libz.so.1.2.13 %{buildroot}%{_libdir}/libz.so
    # just in case we ever package the static library
    mv %{buildroot}/%{_lib}/libz.a %{buildroot}%{_libdir}/

The `install` commands creates `/usr/lib`, the `sed` command fixes the
`zlib.pc` file and then the `pkgconfig` directory is put in the proper
place.

The original `/lib/libz.so` symbolic link is deleted, and a new one is
created within `/usr/lib` that points to the actual library that is
still within `/lib`.

Even though I am not currently packaging the `libz.a` static library,
it is moved into `/usr/lib` just in case there ever arises a legitimate
use case to package the static library.

Within the `%files devel` section, I exclude it from being packages:

    %exclude %{_libdir}/libz.a

Most shared libraries belong in `/usr/lib` and this adjustment is not
necessary.

