LLVM and RUST NOTES
===================

At least currently, the inclusion of the `rustc` compiler (and the llvm
dependency) is purely for the build system. For example, the python
cryptography package requires a rust compiler to build.

Hobbyists and users who need LLVM and/or rust should *probably* build
their own rather than use the packages, perhaps if there is enough demand
then a repository could be spawned for it with better build options to
suit the needs of those who use them.

Rust requires an OpenSSL API to build (maybe can be disabled?) and has
not yet caught up with LibreSSL 3.7.2.

That will happen apparently in July with the changes already queued for
the [1.71.0](https://github.com/rust-lang/rust/pull/110951) build of
rustc.

However for me that is a bit problematic. If it takes that long for a
new stable series of LibreSSL to be supported in the released version
of rustc even though support has been added in a development branch,
then I may need to learn how to merge the development changes into the
released version. It is also problematic because sometimes newer versions
of rustc break the ability to build something and built just fine with
an earlier version of rustc.

I do __not__ want to be forced to delay adopting a new LibreSSL version
just because a package intended for the build system does not yet have
support for it.

It looks like a rust compiler is coming to GCC and may even be usable
by the GCC 14 series---which I suspect will be out before I have a YJL
installer.

As far as compiling the python cryptography package, hopefully using
a GCC rust compiler when it is ready would be good enough.

For the present, there will not be an installer by July 2023 so waiting
for rustc 1.71.0 at present is not *too* problematic.
