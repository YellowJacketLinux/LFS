The Motivation for YJL
======================

In the old days when non-avian dinosaurs walked the earth, Red Hat had
a decent end-user distribution called Red Hat Linux. I got my start in
Linux using MKLinux DR3 which basically was Red Hat 5.1 ported to the
Mach Microkernel.

Well, by decent end-user distribution, we will not talk about Red Hat 7
and the GCC 2.98 debacle...

Sometime later, when yum came into being, third party package repositories
become common with Fedora Extras being the most popular. Those were good
days.

Sometime later, the desktop end-user distribution became Fedora and with
it came a very rapid release cycle with a quick EOL (End Of Life) and
the focus seemed to change, with Fedora basically becoming a testing
ground for what was going to be included in the next RHEL. I became
disenfranchised with Fedora, and constantly needing to install a new
buggy version because the version I had been using when EOL as soon as
the bugs in it seemed to largely be ironed out.

I switched to CentOS 5 which had an incredible lifespan, and stuck with
CentOS 5 until CentOS 7 was released.

CentOS 7 targets enterprise use but in many respects I used it in a
similar fashion as the old Red Hat plus additional repository system
meaning I maintained my own package repositories for things like FFmpeg,
GStreamer, VLC, PHP, etc. where the CentOS/EPEL versions of those
packages either did not exist or were too old.

CentOS 7 was my base, and when I needed something more modern than what
it shipped with, I built it (using GCC 5.x in `/opt` when GCC 4.x was
too old, e.g. for building Audacity).

CentOS 7 will go EOL on June 30, 2024 (just over a year from now),
CentOS 8 is already EOL (as of December 31, 2021), and when CentOS 7
goes EOL people will be forced into CentOS Stream which I really have
no interest in. It looks like it is a QA distro for RHEL, so that the
users are basically unpaid testers for RHEL.

Frack that. I do not want to be a free tester for their commercial
product they profit from.

Linux From Scratch
------------------

I had done the Linux From Scratch (LFS) project a couple times in the
past as part of learning Linux, so I decided that I wanted to just do
Linux From Scratch as my desktop distribution without an upstream
vendor telling me I have to move to a new product. I can upgrade it
when I feel like it.

LFS lacks a package manager. There are several options available, but
I am already fond of the RPM Package Manager (RPM).

This git repository contains the RPM spec files for my RPM bootstrapping
of LFS 11.3 with just enough additional packages for a basic TLS capable
networking (based on GnuTLS as the TLS stack) and RPM itself with the
dependencies needed to build RPM.

This may remain a personal project forever but I do hope to eventually
(as in before June 30, 2024) have both a decent desktop environment
and an installer, potentially allowing this to become a community
driven “Socialist GNU/Linux” (users own the means to production) that
is not driven or steered by capitalist interests as that is what I
blame the demise of Red Hat on.

Note that Fedora is actually a very good distribution for numerous use
cases, it is just I felt really left out of those cases. I think it
is possible to still meet many of those use cases without taking the
direction Fedora took when Fedora Extras went away and the Red Hat
distribution for desktop end users became Fedora.

Please note I would not be able to spend the time I am spending on
this without a benefactor who like me is saddened that the EOL of
CentOS 7 seems to be the EOL of an era.

Also please note I would not be able to create this project without
the Free Software Movement having resulted in a large collection of
high-quality FLOSS (Free-Libre Open Source Software).

Servers will run on this when I am done, but servers really should
have SELinux and I have no interest in SELinux for Desktop users,
which is my target.

Use a commercial distribution for your server needs, preferably one
with a support contract and experienced coders who can deal with both
security and usability bugs in a timely manner.

EOF

