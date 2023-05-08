DH Paramaters
=============

It is the opinion of the LibreSSL packager that whenever possible, DHE
key exchange should be avoided and ECDHE key exchange should be used
instead.

Some TLS clients do not support ECDHE key exchange, so DHE may still
need to be supported on some servers.

MODP IKE DH Paramaters
----------------------

RFC 3526 defines several Diffie-Hellman groups for the Internet Key
Exchange (IKE) protocol.

The RFC may be retrieved at https://www.ietf.org/rfc/rfc3526.txt

From that RFC, the following DH groups are provided in PEM format:

* `/etc/pki/tls/MODP-IKE-2048-group14.pem`
* `/etc/pki/tls/MODP-IKE-3072-group15.pem`
* `/etc/pki/tls/MODP-IKE-4096-group16.pem`
* `/etc/pki/tls/MODP-IKE-6144-group17.pem`
* `/etc/pki/tls/MODP-IKE-8192-group18.pem`

The `.pem` files were retrieved from https://bettercrypto.org/static/dhparams/

At this point in time it is no longer recommended to use DH groups less
than 2048-bit and if you must, they should be uniquely generated and
fairly frequently so. For this reason, the 1536-bit MODP parameters are
not included here.

LibreSSL DH Parameters
----------------------

DH parameters < 1024-bit should never be used and are not supported by
the LibreSSL library. They are vulnerable to the logjam attack, see
https://weakdh.org/ for more information.

DH parameters < 2048-bit should not be used but a few TLS clients still
in use do not support DH parameters > 1024-bit. When using a 1024-bit
group to satisfy those clients it is important that they are unique to
your server and are re-generated frequently.

YJL provides a cron script in `/etc/cron.daily` that will generate a
fresh 2048-bit group on a daily basis, and a cron script in
`/etc/cron.monthly` that will generate fresh 3072-bit and 4096-bit
groups on a monthly basis.

The results of those scripts are placed in the following PEM format
files:

* `/etc/pki/tls/dh2048.pem`
* `/etc/pki/tls/dh3072.pem`
* `/etc/pki/tls/dh4096.pem`

The initial group in the `dh2048.pem`, `dh3072.pem`, and `dh4096.pem`
files are the same as the MODP-IKE parameters. The group in the
`dh2048.pem` file will be replaced by a fresh unique group generated
on your server within a day of install, and the groups in the `dh3072.pem`
and `dh4096.pem` files will be replaced by fresh unique groups within
a month of install.

Which to Use?
-------------

If you must use a 1024-bit group, you will need to generate it youself.
I would recommend regenerating it at least four times a day.

For 2048-bit, 3072-bit, 4096-bit you have a choice. Some prefer the
pre-defined MODP-IKE parameters as they have likely been reviewed by
many eyes, while others prefer parameters uniquely generated on the
server.

It is hypothetically possible unique parameters have a flaw that can
be exploited (e.g. not truly prime and can be factored) but it is very
unlikely.

Similarly it is possible an attack has been crafted for the RFC published
DH parameters, though that also is unlikely as it would almost certainly
take more computing power than even the NSA has to even develop an attack
against the published 2048-bit group.

My *personal* preference is to use the `dh2048.pem` parameters that are
daily re-generated on the server when I need to support DHE key exchange.
The rationale I use is that if an attack ever is developed, it provides
a moving target rather than a static target.

If security beyond what the `dh4096.pem` parameters can provide is
required, then I require ECDHE key exchange.

EOF
