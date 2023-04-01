TeXLive 2023 in LFS 11.3
========================

This document is not yet finished.

This document was written for TeXLive 2023 in LFS 11.3 but probably is
mostly applicable to other versions of LFS and to future versions of
TeXLive as well.

This document and the script within I consider to be Public Domain but
if you must have an actual license, Creative Commons CC0 works for me.


Rationale
---------

On an LFS system, software is generally installed from source. It is
possible to build TeXLive from source but under some situations, it
is *impractical* to do so.

TeXLive is a large collection of mostly architecture independent text
files and fonts from CTAN---The Comprehensive TeX Network. TeXLive
does include a small number of compiled binaries.

Given the massive amount of architexture independent files, it often
makes sense to share a single TeXLive install between multiple operating
systems on the same physical computer, between multiple operating systems
on physically different computers all connected via the same LAN (via
NFS), or by installing TeXLive to a dedicated portable hard drive that
can be taken from place to place and connected to whichever computer
the TeX author is currently using.

Furthermore, for people who use LaTeX a lot, it often makes sense to
have multiple versions of TeXLive available. A documented authored
using TeXLive 2016 may not properly build in TeXLive 2023 without some
time-consuming tweaks to the LaTeX code itself. If such a document
needs a minor edit, it is better to have the version of TeXLive the
LaTeX was originally authored under available than to have to potentially
spend hours updating LaTeX code.

This document explains installing and maintaining a TeXLive system in
LFS that can be shared with other operating systems, even on platforms
other than GNU/Linux.


TeXLive Mountpoint
------------------

Traditionally, the `/opt` filesystem is used for third-party products
that are maintained and updated *outside* of the operating system package
manager.

The typical structure is `/opt/<vendor>/<product>` and TeXLive fits
that paradigm perfectly.

The default install location is actually within `/usr/local` however
`/usr/local` generally should be reserved for software built locally
from source that is not under the control of the package manager.

As the root user, create the directory `/opt/texlive`:

    mkdir -p /opt/texlive

If you will be sharing the TeXLive install between multiple operating
systems on the *same* hardware, you will want to either create a
partition on an internal drive or alternative create a partition on
an external drive.

If you will be sharing the TeXLive install via NFS with other operating
systems on your LAN, you probably should use a partition on an internal
drive.

If you will be sharing the TeXLive install with other operating systems
by use of an external drive, you should use an external drive. Even a
USB thumb drive works.

If you are not sharing the TeXLive install then a separate partition
is not necessary.

For a separate partition, I recommend at least 25 GiB but I prefer 64 GiB
personally. TeXLive actually only needs about 7 GiB but having a larger
partition allows you to have multiple versions installed at the same
time.

I recommend using the `ext2` filesystem. TeXLive does not really benefit
from a journaled file system and especially if you are sharing it with
operating systems other than GNU/Linux, it is usually easier to find
software solutions for mounting `ext2` than for `ext4` or other modern
GNU/Linux filesystems.

Once your partition is properly created and formatted, go ahead and
mount it at the `/opt/texlive` mount point.

If TeXLive is on an external drive, you want the `/etc/fstab` to auto-mount
it when detectected but not attempt to mount it when not present:

    UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX /opt/texlive   ext2  defaults,noauto 1 2

If TeXLive is on an internal drive, then you do want it to auto-mount
during boot:

    UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX /opt/texlive   ext2  defaults 1 2

Obviously replace `XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` with the
actual UUID (which you can find wuth the `blkid` command).

With the partition mounted, go ahead and create the following three
directories:

    mkdir -p /opt/texlive/{2023,texmf-local,tladmin}

The first is where TeXLive 2023 will be installed. The second is for
local additions to the TeXLive system, such as additional fonts and macro
packages like [MathTime Pro 2](https://www.pctex.com/mtpro2.html). The
third is a home directory for the TeXLive administrative user. Keeping
the home directory for that user on the same partition as the TeXLive
install allows you to easily administrate the install from any Un*x
operating system the partition is mounted on---should you choose to
do so.


TeXLive User and Group
----------------------

The next thing to do is create a `texlive` user and group. The purpose
of the group is two-fold:

1. It provides a group for the texlive administrator.
2. It provides a group for users of the texlive system.

When TeXLive is available, *any* user on the system can use it by simply
adjusting their PATH environmental variable. For users that *want* to
use the TeXLive system, it is easier if the environmental variables are
already set up for them when they log in.

By adding users who *want* to use the TeXLive system to the `texlive`
group, those users can automatically have their environmental variables
(PATH, INFOPATH, MANPATH) adjust to use the TeXLive system while other
user accounts (including system users and daemons) that do not need
to use the TeXLive system do not have their environmental variables
adjusted.

The purpose of the `texlive` user is to have an otherwise unprivileged
user account that installs and administrates the TeXLive system.

When sharing a TeXLive install, each Un*x system should have both the
`texlive` user and group and they should have the same user-id and
group-id, at least if you wish to be able to be able to also administrate
the TeXLive system from any Un*x system using the partition.

The UID/GID I personally use is `450` for both. The reason I chose
`450` is because it is well above `100` (under `100` is usually used
for system users and daemons) yet below 500. Most Un*x systems today
start user accounts at `1000` but some use `500` as the first personal
account UID/GID, so I chose `450` to specifically be below that.

When creating the `texlive` user, make sure to set the home directory
to `/opt/texlive/tladmin` and the shell to `/bin/bash` (or to `/usr/bin/bash`
on systems that put `bash` in `/usr/bin`).

I personally do not set a password for the `texlive` user. You can
become the `texlive` user by first logging in to the `root` account
and then issuing the following command:

    su - texlive

If you have [sudo](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/sudo.html)
installed, then users in the `wheel` group can become the texlive
user with the following command:

    sudo su - texlive

Note that you only need to become the `texlive` user to administer the
system. Usually that means once a month or so, installing updates. Or
whenever you think you come across a bug, to see if it is already fixed
before reporting it.

As the root user, copy the relevant `/etc/skel` files into the `/opt/texlive/tladmin`
directory:

    cp /etc/skel/{.bash_logout,.bash_profile,.bashrc} /opt/texlive/tladmin/

Finally, set the correct permissions:

    chown -R texlive:texlive /opt/texlive/tladmin
    chown texlive:texlive /opt/texlive/{2023,texmf-local}

You are now ready to install TeXLive 2023.


Install TeXLive 2023
--------------------

foo



/etc/profile.d/texlive.sh
-------------------------

The following script is what I use to set up the various environmental
variables for TeXLive in LFS. It is an adaptation of a script I first
wrote for use in CentOS since TeXLive 2014, the adaptation being I used
the `pathprepend` function from the BLFS bash `/etc/profile` script.

This script only sets up the path for non-root users of the `texlive`
group, and it does not need to be updated when you update TeXLive
itself to a new version.

    # /etc/profile.d/texlive.sh - set *PATH variables for TeXLive

    checkuser () {
      ### returns 0 only for non-root members of texlive group
      if [ "`id -u`" == "0" ]; then
        return 1
      fi
      TLGID="`id -g texlive`" 2> /dev/null
      if [ $? -ne 0 ]; then
        return 1
      fi
      for id in `id -G`; do
        if [ "${id}" == "${TLGID}" ]; then
          return 0
        fi
      done
      return 1
    }

    tlversion () {
      ### returns 0 only if it finds an ls-R in texmf-dist
      ### only checks for versions within last seven years.
      YYYY=`date +%Y`
      for n in 0 1 2 3 4 5 6 7; do
        DIR="`echo "${YYYY} - ${n}" |bc`"
        if [ -f /opt/texlive/${DIR}/texmf-dist/ls-R ]; then
          printf ${DIR}
          return 0
        fi
      done
      return 1
    }

    tlplatform () {
      HARDWARE="`uname -m`"
      OS="`uname -o`"
      case "${OS}" in
        GNU/Linux)
          case "${HARDWARE}" in
            x86_64)
              printf "x86_64-linux"
              ;;
            arm64)
              printf "aarch64-linux"
              ;;
            i386 | i486 | i586 | i686)
              printf "i386-linux"
              ;;
            *)
              # hardware not (yet) supported by script
              return 1
              ;;
          esac
          ;;
        *)
          # OS not (yet) supported by script
          return 1
          ;;
      esac
      return 0
    }

    if checkuser; then
      TLPLATFORM="`tlplatform`"
      if [ $? -eq 0 ]; then
        TLIVEV="`tlversion`"
        if [ $? -eq 0 ]; then
          # pathprepend defined in BLFS/YJL /etc/profile
          pathprepend /opt/texlive/${TLIVEV}/bin/${TLPLATFORM}
          pathprepend /opt/texlive/${TLIVEV}/texmf-dist/doc/info INFOPATH
          pathprepend /opt/texlive/${TLIVEV}/texmf-dist/doc/man MANPATH
        fi
      fi
    fi

    # End /etc/profile.d/texlive.sh

With that file installed within `/etc/profile.d` LFS should automatically
set up the environmental variables for users within the `texlive` group
to use the TeXLive system. At least for users who use `bash` as their
login shell.

An equivalent for `tcsh` has not (yet) been written.

Missing Libraries
-----------------

With a barebones LFS install, the following TeXLive 2023 installed
binaries have missing shared library dependencies.

Note that without these libraries installed, I was able to use TeXLive
2023 within LFS 11.3 to compile TeX projects originally authored in
LuaLaTeX without any problems.

Most if not all of the missing shared library dependencies will be met
once an LFS/BLFS 11.3 system has the X11 windowing system installed.

I do not believe TeXLive has been ported to pure Wayland yet.

### xetex

This is probably the most important component of TeXLive to support
even if you do not use it yourself, it is quite likely that at some
point you will need to compile a LaTeX document written for XeTeX if
you are involved at all in the TeX world.

The missing libraries after a barebones LFS install are:

  * libfontconfig.so.1
  * libfreetype.so.6

Relevant BLFS packages:

  * [FreeType2](https://www.linuxfromscratch.org/blfs/view/stable/general/freetype2.html)
  * [Fontconfig](https://www.linuxfromscratch.org/blfs/view/stable/general/fontconfig.html)

### metafont

The `mf` program is metafont and is used to generate TeX native fonts.
In this day in age, generally OpenType fonts are used for new LaTeX
projects and at least with LuaLaTeX, a barebones LFS install has what
is needed to deal with those. However sometimes older LaTeX projects
will want metafont available. My *memory* is that when compiling a
document that uses Type 1 (Postscript) fonts and the font was not
present, the LaTeX compiler itself would call metafont to compile a
substitute from metafont source at the needed DPI. It is probably a
good idea to have metafont working.

The missing libraries after a barebones LFS install are:

  * libSM.so.6
  * libICE.so.6
  * libXext.so.6
  * libX11.so.6

### Asymptote

Most users probably do not need this to work.

The `asy` command invokes a script-based vector graphics language for
generating technical drawings. It can be used to create very high
quality figures. At this point, most high quality figures are actually
generated as postscript or PDF images using programs outside of the
TeXLive system, but it is *possible* you may need this command to work
especially if you are working with older TeX projects.

The missing libraries after a barebones LFS install are:

  * libGLX.so.0
  * libglut.so.3
  * libGL.so.1

### xdvi-xaw

In the old days, the standard way to use a TeX system was to generate
a DVI file that could then be sent to be printed or rendered by a device
with an appropriate DVI driver.

When generating a postscript file, one would then use the program dvips
to create a postscript file from the DVI file.

DVI files are rarely generated now, but when they are generated you may
want the `xdvi-xaw` program to view the DVI file on your display before
it is printed or further processed into something else.

The missing libraries after a barebones LFS install are:

  * libXaw.so.7
  * libXmu.so.6
  * libXt.so.6
  * libSM.so.6
  * libICE.so.6
  * libXext.so.6
  * libXpm.so.4
  * libX11.so.6

### pdfclose, pdfopen

Those two programs are not needed on GNU/Linux.

The missing library if you want them to work anyway is:

  * libX11.so.6


