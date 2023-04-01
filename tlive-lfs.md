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


TeXLive User and Group
----------------------

The first thing to do is create a `texlive` user and group. The purpose
of the group is two-fold.

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

### xetex

This is probably the most important component of TeXLive to support
even if you do not use it yourself, it is quite likely that at some
point you will need to compile a LaTeX document written for XeTeX if
you are involved at all in the TeX world.

The missing libraries after a barebones LFS install are:

  * libfontconfig.so.1
  * libfreetype.so.6

### metafont

The mf program is metafont and is used to generate TeX native fonts.
In this day in age, generally OpenType fonts are used for new LaTeX
projects and at least with LuaLaTeX, a barebones LFS install has what
is needed to deal with those. However sometimes older LaTeX projects
will want metafont available. My *memory* is that when compiling a
document that uses Type 1 (Postscript) fonts and the font was not
present, the LaTeX compiler itself would call metafont to compile a
substitute from metafont source at the needed DPI. It's probably a
good idea to have metafont working.

The missing libraries after a barebones LFS install are:

  * libSM.so.6
  * libICE.so.6
  * libXext.so.6
  * libX11.so.6

### Asymptote

Most users probably do not need this to work.

The asy command invokes a script-based vector graphics language for
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
want the xdvi-xaw program to view the DVI file on your display before
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


