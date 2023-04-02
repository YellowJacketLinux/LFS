TeXLive 2023 in LFS 11.3
========================

This document is not yet finished.

This document was written for TeXLive 2023 in LFS 11.3 but probably is
mostly applicable to other versions of LFS and to future versions of
TeXLive as well.

This document and the script within I consider to be Public Domain but
if you must have an actual license, Creative Commons CC0 works for me.

These instructions were tried on a very basic LFS 11.3 system with
just a few additions from BLFS, the important addition being
[curl](https://www.linuxfromscratch.org/blfs/view/stable/basicnet/curl.html)
which I chose to build against
[GnuTLS](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/gnutls.html)
for TLS support. Building `curl` against OpenSSL (or LibreSSL) should also
work.

You should also have [GnuPG](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/gnupg.html)
before installing TeXLive 2023 for package verification (performed
automatically by the TeXLive installer/updater).

These instructions also assume you have gone through the BLFS
[After LFS Configuration Issues](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/config.html)
section and have implemented
[The Bash Shell Startup Files](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/profile.html)
section.

Other dependencies can be resolved after install as needed.


Rationale
---------

On an LFS system, software is generally installed from source. It is
possible to build TeXLive from source but under some situations, it
is *impractical* to do so.

TeXLive is a large collection of mostly architecture independent text
files and fonts from CTAN---The Comprehensive TeX Archive Network.
TeXLive does include a small number of compiled binaries.

Given the massive amount of architexture independent files, it often
makes sense to share a single TeXLive install between multiple operating
systems on the same physical computer, between multiple operating systems
on physically different computers all connected via the same LAN (via
NFS), or by installing TeXLive to a dedicated portable hard drive that
can be taken from place to place and connected to whichever computer
the TeX author is currently using.

Furthermore, for people who use LaTeX a lot, it often makes sense to
have multiple versions of TeXLive available. A document authored using
TeXLive 2016 may not properly build in TeXLive 2023 without some
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
from source that is not under the control of a package manager.

As the root user, create the directory `/opt/texlive`:

    mkdir -p /opt/texlive

If you will be sharing the TeXLive install between multiple operating
systems on the *same* hardware, you will want to either create a
partition on an internal drive or alternatively create a partition on
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

Once your partition has been properly created and formatted, go ahead
and mount it at the `/opt/texlive` mount point.

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
install allows you to easily administrate the install from any Unix
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
(PATH, INFOPATH, MANPATH) adjusted to use the TeXLive system while other
user accounts (including system users and daemons) that do not need
to use the TeXLive system do not have their environmental variables
adjusted.

The purpose of the `texlive` user is to have an otherwise unprivileged
user account that installs and administrates the TeXLive system.

When sharing a TeXLive install, each Unix system should have both the
`texlive` user and group and they should have the same user-id and
group-id, at least if you wish to be able to be able to also administrate
the TeXLive system from any Unix system using the partition.

The UID/GID I personally use is `450` for both. The reason I chose
`450` is because it is well above `100` (under `100` is usually used
for system users and daemons) yet below 500. Most Unix systems today
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
installed *with the default BLFS configuration*, then users in the
`wheel` group can become the texlive user with the following command:

    sudo su - texlive

That is my preferred method.

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

To install TeXLive 2023, first become the `texlive` user:

    sudo su - texlive

As the `texlive` user, retrieve the installer:

    TMPDIR="`mktemp --tmpdir -d tlive-XXXXXXXXXXXX`"
    pushd ${TMPDIR}
    curl -L -O https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz

Note the `-L` option is necessary because it will redirect you to a mirror.

Unpack the archive, enter the installer directory, and install it:

    tar -zxf install-tl-unx.tar.gz
    cd install-tl-20*
    /usr/bin/perl ./install-tl                \
      --texdir="/opt/texlive/2023"            \
      --texmflocal="/opt/texlive/texmf-local" \
      --no-interaction

There are some other options (such as default papersize) but those can
be set after install. Normally I like to set papersize in the document
itself however ff you plan to use TeXLive to build documentation that
comes with source packages in LFS/BLFS, you probably want to set the
default papersize to the size of paper your printer uses.

That is covered in the [Paper Size](#paper-size) section.

The install will likely take an hour or so, depending upon the speed
of the mirror used for the install.

Once installed, remove the temporary install directory:

    popd
    # optionally - since in /tmp it should be deleted automatically eventually
    rm -rf ${TMPDIR}


/etc/profile.d/texlive.sh
-------------------------

The following script is what I use to set up the various environmental
variables for TeXLive in LFS. It is an adaptation of a script I first
wrote for use in CentOS for TeXLive 2014, the adaptation being I used
the `pathappend` function from the BLFS bash `/etc/profile` script.
See [The Bash Shell Startup Files](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/profile.html)
in the BLFS book.

This script only sets up the path for non-root users of the `texlive`
group, and it does not need to be updated when you update TeXLive
itself to a new version, it always adjusts to the newest version
of TeXLive installed.

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
          # pathappend defined in BLFS/YJL /etc/profile
          pathappend /opt/texlive/${TLIVEV}/bin/${TLPLATFORM}
          pathappend /opt/texlive/${TLIVEV}/texmf-dist/doc/info INFOPATH
          pathappend /opt/texlive/${TLIVEV}/texmf-dist/doc/man MANPATH
        fi
      fi
    fi

    # End /etc/profile.d/texlive.sh

With that file installed within `/etc/profile.d` LFS should automatically
set up the environmental variables for users within the `texlive` group
to use the TeXLive system. At least for users who use `bash` as their
login shell.

An equivalent for `tcsh` has not (yet) been written.

Note to use this method for setting up the environmental variables on
other GNU/Linux distributions (or other operating systems) you will
likely have to port it. CentOS/Fedora for example do not define the
`pathappend` function, and on macOS the appropriate place to mount
the partition is probably `/usr/local/opt/texlive` rather than `/opt/texlive`.
Or maybe `/Volumes/texlive`. Just pick one... 😜

If you would prefer to have the texlive environmental variables set
for *every* login user (except `root`) *without* needing to put every
login user in the `texlive` group, just have the `checkuser ()` function
return `0` for the `texlive` user and for any user with a UID greater
than `999`.

I highly recommend against modifying the environmental variables for
the root user, or for system/daemon users, for security reasons.


Post Install Administration
---------------------------

### Updates

Periodically it is a good idea to apply updates to the TeXLive system.
When the `tlmgr` command itself needs an update, it generally has to
be updated by itself before any other packages can be updated.

To keep my system up to date, I have the following shell script in
`/opt/texlive/tladmin` and run it as the `texlive` user about once a
month, or whenever I think about it:

    #!/usr/bin/env bash
    #  Begin update-tl.sh
    #
    tlmgr update --self
    if [ $? -eq 0 ]; then
      tlmgr update --all
    fi
    #  End update-tl.sh

I use `#!/usr/bin/env bash` as the shebang because I do not know what
operating system I might want to run it from, or where that operating
system has `bash` installed.

### Local Files

If you have any macros or macro files that are not part of TeXLive,
put them in the `/opt/texlive/texmf-local` tree and then as the
`texlive` user, run the command `texhash` to update the `ls-R` file
in `texmf-local` so that TeXLive knows where to find the files.

If any of the fonts need a fontmap file enabled, use the `updmap-sys`
variant of `updmap` to enable them so that they are enabled for all
users regardless of which operating system has the TeXLive partition
mounted.

### Paper Size

By default, a TeXLive install will use the A4 paper size for documents
that do not specify a paper size.

Generally it is a good idea to *always* set the intended paper size
in your project but for projects intended to be compiled anywhere---as
is the case with open source software documentation---it is better not
to specify the paper size so that the documentation can be built to
match the paper size it is most likely to be printed on.

If you are in the United States and would prefer U.S. Letter to A4 when
the document does not specify the paper size, run the following command:

    tlmgr paper letter

If you need to change it back to A4:

    tlmgr paper a4

### Binary Platform Support

By default, the TeXLive installer only installs binaries for one
platform. If you need support for another platform, you can install
support for an additional platform.

To see all available platform options as well as which platforms are
already installed, use the command:

    tlmgr platform list

To add an available platform, use `tlmgr add <platform>`. For example,
to add support for macOS so that you can share the TeXLive install with
macOS, you would run the command:

    tlmgr platform add universal-darwin

If you need to remove a platform you are no longer using, then you can
use the same command to add the platform, substituting `remove` in
place of `add`.

### Adobe Base 35 Fonts

Most people can skip this.

TeXLive ships with the metric compatible URW clones of the Adobe Base35
Postscript Level 2 fonts.

If you happen to have the genuine Adobe Base35 fonts installed in the
proper place within your `texmf-local` tree:

    texmf-local/fonts/type1/adobe/base35/

Then you can configure TeXLive to use the genuine Adobe fonts. If they
are named using the "berry" names (e.g. phvbo8an.pfb):

    updmap-sys --setoption LW35 ADOBEkb

On the other hand if they have the Adobe vendor filenames
(e.g. `hvnbo___.pfb`):

    updmap-sys --setoption LW35 ADOBE

Visually, almost no one can tell the difference between the free URW
clones and the genuine Adobe fonts, but if you happen to have the
genuine Adobe fonts you might as well use them for projects that call
the Base35 postscript fonts.

Modern LaTeX projects that want to use fonts of the Base35 look and feel
generally should use the
[TeX Gyre](https://www.gust.org.pl/projects/e-foundry/tex-gyre/index_html)
OpenType fonts instead, as they have *much better* glyph coverage, but
some macro packages which have an internal need to typeset characters
(such as the packages for generating barcodes) will still specify the
actual Base35 fonts internally for backwards compatibility, and some
open source software with LaTeX documentation uses the Baes35 fonts.

### Commercial Math Fonts

If you are not writing for a commercial publication, the free math
fonts that are part of TeXLive almost certainly meet your needs. See
[CTAN Maths Font](https://ctan.org/topic/font-maths).

Commercial publications however often have an established workflow
and like to specify what macro packages and fonts you are allowed to
use in order to be allowed to make them money.

Some publications will require you to use
[MathTime Pro 2](https://www.pctex.com/mtpro2.html) for your math font
(usually in combination with `times.sty` as your main body font)
and other publications will require you use the
[Lucida Fonts](https://tug.org/store/lucida/index.html).

If you are writing for such a publication, the proper place to install
the files is within the `/opt/texlive/texmf-local` tree.

Both packages come with install instructions but in both cases I often
see some users confused.

1. First put the files in their proper place within the `texmf-local`
   tree.
2. Then *as the `texlive` user* run the `texhash` command.
3. then *as the `texlive` user* run the `updmap-sys` variant of the
   `updmap` command when enabling the font map file. Otherwise the fonts
   will not be system-wide enabled for all users.

When you upgrade to a new version of TeXLive, you do not need to
re-install those packages, but you will need to re-run the appropriate
`updmap-sys` command to re-enable the needed map file in the new version
of TeXLive.

LFS Missing Libraries
---------------------

With a barebones LFS install, the following TeXLive 2023 installed
binaries have missing shared library dependencies.

Note that without these libraries installed, I was able to use TeXLive
2023 within LFS 11.3 to compile TeX projects originally authored for
LuaLaTeX compilation without any problems.

Most if not all of the missing shared library dependencies will be met
once an LFS/BLFS 11.3 system has the X11 windowing system installed.

### xetex

This is probably the most important component of TeXLive to support
even if you do not use it yourself, it is quite likely that at some
point you will need to compile a LaTeX document written for XeLaTeX if
you are involved at all in the TeX world.

The missing libraries after a barebones LFS install are:

  * libfontconfig.so.1
  * libfreetype.so.6

Relevant BLFS packages:

  * [FreeType2](https://www.linuxfromscratch.org/blfs/view/stable/general/freetype2.html)
  * [Fontconfig](https://www.linuxfromscratch.org/blfs/view/stable/general/fontconfig.html)

### metafont

The `mf` program is metafont and is used to generate TeX native fonts.
In this day in age, generally vector fonts (Type 1, TrueType, OpenType)
are used for new LaTeX projects and at least with LuaLaTeX, a barebones
LFS install has what is needed to deal with those. However sometimes older
LaTeX projects will want metafont available.

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

If you need Asymptote, I recommend building it independently of TeXLive.
See BLFS [Asymptote](https://www.linuxfromscratch.org/blfs/view/stable/pst/asymptote.html).

You can then remove the binary from TeXLive. As the `texlive` user:

    tlmgr remove asymptote.x86_64-linux --no-depends-at-all

However understand that doing so will mean `asy` may not be available
to other x86_64-linux operating systems unless they too have the binary
installed separate from TeXLive.

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


Ghostscript
-----------

Even though modern TeX engines can output directly to PDF and ghostscript
is no longer plays the same role in a TeX workflow that it used to play,
you will at some point find yourself needing to install
[Ghostscript](https://www.linuxfromscratch.org/blfs/view/stable/pst/gs.html).


Python2 Issues
--------------

Python2 is officially deprecated. Unfortunately, a handful of scripts
in TeXLive 2023 have not yet been ported to Python 3 (or possibly work
with both Python 2 and Python 3) and even worse, those scripts call the
ambiguous generic `python` instead of `python2`.

If you need those scripts for your LaTeX workflow, install
[Python2](https://www.linuxfromscratch.org/blfs/view/stable/general/python2.html)
on your LFS system. I recommend using a prefix of `/opt/legacy/python2`
and then adding `/opt/legacy/python2/bin` to the path of any user
that needs any of those scripts.

you can then make `/opt/legacy/python2/bin/python` be a symbolic link
to `/opt/legacy/python2/bin/python2.7`. As the `root` user:

    ln -sf python2.7 /opt/legacy/python2/bin/python

Then *most* of the TeXLive scripts that call an unversioned `python`
will work as long as `/opt/legacy/python2/bin` is in the `PATH` of the
users that needs it.

You can accomplish this by adding the following to `/etc/profile.d/texlive.sh`
where the other calls to `pathappend` occur:

    pathappend /opt/legacy/python2/bin

The scripts that work with this method all use the following shebang:

    #!/usr/bin/env python

Some of the scripts with that shebang *might* work with Python 3 but
I do not know which scripts they are. They supposedly all work with
Python 2.7.

### The `de-macro` Script

The executable script `de-macro` calls `!/usr/bin/python -O` but when
you read the script, it explicitly states that it works with Python 3.

To get it to work in LFS where `/usr/bin/python` does not exist, as
the `texlive` user:

    sed -i 's?/usr/bin/python -O?/usr/bin/python3 -O?' \
      /opt/texlive/2023/bin/x86_64-linux/de-macro

Whenever TeXLive updates that script, unfortunately it will undo the
change. Hopefully in the near future we can convince the TeXLive
maintainers to specify `python3` for any script that *can* run in
Python 3.


Ruby Dependency
---------------

A few executable scripts depend upon Ruby. If you need those scripts,
install [Ruby](https://www.linuxfromscratch.org/blfs/view/stable/general/ruby.html).


Wish Dependency
---------------

A few executable scripts depend upon `wish` which is provided by Tk.
If you need those scripts, install
[Tk](https://www.linuxfromscratch.org/blfs/view/stable/general/tk.html).
Note that Tk requires the X11 system.


SNOBOL4 Dependency
------------------

A single script, `texaccents`, requires `snobol4`. It does not seem to
be part of BLFS but can be found at (https://www.regressive.org/snobol4/csnobol4/curr/).


Text Editors
------------
To compose your LaTeX projects, you need a text editor you know how
to use, preferably one with LaTeX syntax highlighting.

When using UTF-8 (as you should for anything new), the text editor should
not insert a BOM (Byte Order Mark) at the beginning of the document.

Allegedly a BOM is no longer a problem in TeXLive since TeXLive 2018
but I have not verified that always is the case, and it probably is
not the case for some commercial TeX distributions that publishers
often use.

Use a text editor that does not insert a BOM.

### Traditional Unix-like Operating Systems CLI

The `vim` editor that is part of LFS is sufficient but if you do a *lot*
of work in LaTeX it may be worth your time to learn how to use
[GNU Emacs](https://www.linuxfromscratch.org/blfs/view/stable/postlfs/emacs.html).

### Traditional Unix-like Operating Systems GUI

For a GUI editor, I *really* like LaTeXila but the project first was
integrated in GNOME3 as [GNOME-LaTeX](https://gitlab.gnome.org/swilmet/gnome-latex)
and then it appears the original author has left or been pushed out.

I just use LaTeXila 3.26.1 and do not bother updating it, I am not a
fan of GNOME 3.

LaTeXila 3.26.1 builds and works well in [MATE](https://mate-desktop.org/).
Unfortunately I do not know of a current mirror that still hosts the
LaTeXila tarballs but it can be found in the old Fedora source RPMs.

### macOS

To share TeXLive as installed here with macOS, you need to be able to
mount `ext2` filesystems. There are several solutions, pick one.

Note that MacTeX is just TeXLive with a few extra GUI programs that I
personally found to be useless. On macOS for a text editor, I highly
recommend using [BBEdit](https://www.barebones.com/products/bbedit/).
The free version works well with LaTeX but BBEdit is worth paying for.

### Windows

It is possible to run TeXLive on Windows but it is *possible* the
Windows installer is actually required.

Most people I know in the LaTeX world who use Windows just use
[MiKTeX](https://miktex.org/) on Windows, and generally use the
[Notepad++](https://notepad-plus-plus.org/downloads/) text editor.

When I have had to use Windows, any projects I was working on in TeXLive
had no problems compiling in MiKTeX, MiKTeX is highly compatible with
TeXLive since both use CTAN for their macro packages. Just be sure that
Notepad++ uses Unix line breaks to avoid projects with mixed line breaks.

A proper UTF-8 text editor without a BOM (Byte Order Mark) is recommended.
Do not try to use Windows Notepad, it always adds a BOM. Use Notepad++
configured to save as UTF-8 without the BOM.
