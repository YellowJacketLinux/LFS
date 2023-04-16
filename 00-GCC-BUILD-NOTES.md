GCC Build Notes
===============

ADA and D Support
-----------------

Ada and D support have already been bootstrapped into my build of
GCC 12.2.0. See

[GCC-Bootstrap](https://github.com/YellowJacketLinux/GCC-Bootstrap)


Go Support
----------

The GCC go compiler builds and works, but there is a warning in the
documentation that the libraries should not be stripped, not even of
debugging symbols.

It looks like it is possible to build the libraries as a separate
package that has stripping disabled, but I have not yet done that.

The plan is to build the go libraries in such a package without them
being stripped, and then rebuild GCC excluding the go libraries and
with full stripping.
