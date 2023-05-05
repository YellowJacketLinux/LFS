%global bashv 5.2.15
%global bcompv 2.11
%global bcompdir %{_datadir}/bash-completion

# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     bash
Version:  5.2.15
Release:  %{?repo}0.rc5%{?dist}
Summary:  The Bourne Again Shell

Group:    System Environment/Shells
License:  GPL-3.0-or-later and GPL-2.0-or-later
URL:      https://gnu.org/software/bash
Source0:  https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:  https://github.com/scop/bash-completion/releases/download/%{bcompv}/bash-completion-%{bcompv}.tar.xz
# These are from BLFS - https://www.linuxfromscratch.org/blfs/view/stable/postlfs/profile.html 2023-03-11
Source11: bash-profile
Source12: bash-bashrc

BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}
Provides: bash-completion

%description
Bash is a Unix shell and scripting language developed for the GNU project as a
replacement for the Bourne shell. Bash is the stanard shell for the GNU/Linux
operating system.

This package also includes bash-completion %{bcompv}.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: bash-completion-devel

%description devel
This package includes the headers and related files needed to build software
that uses bash.

%prep
%setup -c -q
tar -xf %{SOURCE1}


%build
cd bash-%{bashv}
%configure \
  --bindir=/bin \
  --without-bash-malloc \
  --with-installed-readline 
#  --docdir=%{_datadir}/doc/%{name}-%{version}
make %{?_smp_mflags}
cd ../bash-completion-%{bcompv}
%configure
make %{?_smp_mflags}


%install
cd bash-%{bashv}
make install DESTDIR=%{buildroot}

cd ../bash-completion-%{bcompv}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_sysconfdir}/profile.d/bash_completion.sh
cd ..
mkdir bash-completion
for docfile in AUTHORS CHANGES CONTRIBUTING.md COPYING README.md; do
  cp -p bash-completion-%{bcompv}/${docfile} bash-completion/
done
cp -p bash-completion-%{bcompv}/COPYING ./COPYING.bash-completion
cp -p bash-%{bashv}/COPYING ./COPYING.bash
%find_lang %{name}

ln -sf bash %{buildroot}/bin/sh
install -m644 -D %{SOURCE11} %{buildroot}/%{_sysconfdir}/profile
install -m644 %{SOURCE12} %{buildroot}/%{_sysconfdir}/bashrc
install -d %{buildroot}%{_sysconfdir}/profile.d
install -d %{buildroot}%{_sysconfdir}/skel

rm -rf %{buildroot}%{_datadir}/doc/bash

# These are from BLFS - https://www.linuxfromscratch.org/blfs/view/stable/postlfs/profile.html 2023-03-11

cat > %{buildroot}%{_sysconfdir}/profile.d/dircolors.sh << "EOF"
# Setup for /bin/ls and /bin/grep to support color, the alias is in /etc/bashrc.
if [ -f "/etc/dircolors" ] ; then
        eval $(dircolors -b /etc/dircolors)
fi

if [ -f "$HOME/.dircolors" ] ; then
        eval $(dircolors -b $HOME/.dircolors)
fi

alias ls='ls --color=auto'
alias grep='grep --color=auto'
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/extrapaths.sh << "EOF"
if [ -d /usr/local/lib/pkgconfig ] ; then
        pathappend /usr/local/lib/pkgconfig PKG_CONFIG_PATH
fi
if [ -d /usr/local/bin ]; then
        pathprepend /usr/local/bin
fi
if [ -d /usr/local/sbin -a $EUID -eq 0 ]; then
        pathprepend /usr/local/sbin
fi

if [ -d /usr/local/share ]; then
        pathprepend /usr/local/share XDG_DATA_DIRS
fi

# Set some defaults before other applications add to these paths.
pathappend /usr/share/man  MANPATH
pathappend /usr/share/info INFOPATH
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/readline.sh << "EOF"
# Set up the INPUTRC environment variable.
if [ -z "$INPUTRC" -a ! -f "$HOME/.inputrc" ] ; then
        INPUTRC=/etc/inputrc
fi
export INPUTRC
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/umask.sh << "EOF"
# By default, the umask should be set.
if [ "$(id -gn)" = "$(id -un)" -a $EUID -gt 99 ] ; then
  umask 002
else
  umask 022
fi
EOF

# /etc/skel files

cat > %{buildroot}%{_sysconfdir}/skel/.bash_profile << "EOF"
# Begin ~/.bash_profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# updated by Bruce Dubbs <bdubbs@linuxfromscratch.org>

# Personal environment variables and startup programs.

# Personal aliases and functions should go in ~/.bashrc.  System wide
# environment variables and startup programs are in /etc/profile.
# System wide aliases and functions are in /etc/bashrc.

if [ -f "$HOME/.bashrc" ] ; then
  source $HOME/.bashrc
fi

if [ -d "$HOME/bin" ] ; then
  pathprepend $HOME/bin
fi

### python2 path configuration
### Only uncomment below three lines if you really need python2

#if [ -L /opt/legacy/python2/bin/python2 ]; then
#  pathappend /opt/legacy/python2/bin
#fi

### End python2 path configuration

# End ~/.bash_profile
EOF

cat > %{buildroot}%{_sysconfdir}/skel/.profile << "EOF"
# Begin ~/.profile
# Personal environment variables and startup programs.

if [ -d "$HOME/bin" ] ; then
  pathprepend $HOME/bin
fi

# Set up user specific i18n variables
#export LANG=<ll>_<CC>.<charmap><@modifiers>

# End ~/.profile
EOF

cat > %{buildroot}%{_sysconfdir}/skel/.bashrc << "EOF"
# Begin ~/.bashrc
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>

# Personal aliases and functions.

# Personal environment variables and startup programs should go in
# ~/.bash_profile.  System wide environment variables and startup
# programs are in /etc/profile.  System wide aliases and functions are
# in /etc/bashrc.

if [ -f "/etc/bashrc" ] ; then
  source /etc/bashrc
fi

# Set up user specific i18n variables
#export LANG=<ll>_<CC>.<charmap><@modifiers>

# End ~/.bashrc
EOF

cat > %{buildroot}%{_sysconfdir}/skel/.bash_logout << "EOF"
# Begin ~/.bash_logout
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>

# Personal items to perform on logout.

# End ~/.bash_logout
EOF

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /bin/bash
%attr(0755,root,root) /bin/bashbug
/bin/sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/profile
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/bashrc
%dir %attr(0755,root,root) %{_sysconfdir}/profile.d
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/profile.d/*.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/skel/.bash_logout
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/skel/.bash_profile
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/skel/.bashrc
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/skel/.profile
%attr(0755,root,root) %dir %{_prefix}/lib/bash
%attr(0644,root,root) %{_prefix}/lib/bash/Makefile.*
%attr(0644,root,root) %{_prefix}/lib/bash/loadables.h
%attr(0755,root,root) %{_prefix}/lib/bash/accept
%attr(0755,root,root) %{_prefix}/lib/bash/basename
%attr(0755,root,root) %{_prefix}/lib/bash/csv
%attr(0755,root,root) %{_prefix}/lib/bash/cut
%attr(0755,root,root) %{_prefix}/lib/bash/dirname
%attr(0755,root,root) %{_prefix}/lib/bash/dsv
%attr(0755,root,root) %{_prefix}/lib/bash/fdflags
%attr(0755,root,root) %{_prefix}/lib/bash/finfo
%attr(0755,root,root) %{_prefix}/lib/bash/getconf
%attr(0755,root,root) %{_prefix}/lib/bash/head
%attr(0755,root,root) %{_prefix}/lib/bash/id
%attr(0755,root,root) %{_prefix}/lib/bash/ln
%attr(0755,root,root) %{_prefix}/lib/bash/logname
%attr(0755,root,root) %{_prefix}/lib/bash/mkdir
%attr(0755,root,root) %{_prefix}/lib/bash/mkfifo
%attr(0755,root,root) %{_prefix}/lib/bash/mktemp
%attr(0755,root,root) %{_prefix}/lib/bash/mypid
%attr(0755,root,root) %{_prefix}/lib/bash/pathchk
%attr(0755,root,root) %{_prefix}/lib/bash/print
%attr(0755,root,root) %{_prefix}/lib/bash/printenv
%attr(0755,root,root) %{_prefix}/lib/bash/push
%attr(0755,root,root) %{_prefix}/lib/bash/realpath
%attr(0755,root,root) %{_prefix}/lib/bash/rm
%attr(0755,root,root) %{_prefix}/lib/bash/rmdir
%attr(0755,root,root) %{_prefix}/lib/bash/seq
%attr(0755,root,root) %{_prefix}/lib/bash/setpgid
%attr(0755,root,root) %{_prefix}/lib/bash/sleep
%attr(0755,root,root) %{_prefix}/lib/bash/stat
%attr(0755,root,root) %{_prefix}/lib/bash/strftime
%attr(0755,root,root) %{_prefix}/lib/bash/sync
%attr(0755,root,root) %{_prefix}/lib/bash/tee
%attr(0755,root,root) %{_prefix}/lib/bash/truefalse
%attr(0755,root,root) %{_prefix}/lib/bash/tty
%attr(0755,root,root) %{_prefix}/lib/bash/uname
%attr(0755,root,root) %{_prefix}/lib/bash/unlink
%attr(0755,root,root) %{_prefix}/lib/bash/whoami
%attr(0644,root,root) %{_infodir}/bash.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/bash.1*
%attr(0644,root,root) %{_mandir}/man1/bashbug.1*
# %%{_datadir}/doc/%%{name}-%%{version}
# Bash Completion
%dir %{bcompdir}
%attr(0644,root,root) %{bcompdir}/bash_completion
%{bcompdir}/completions
%dir %{bcompdir}/helpers
%attr(0644,root,root) %{bcompdir}/helpers/perl
%attr(0644,root,root) %{bcompdir}/helpers/python
# otro
%license COPYING.bash-completion COPYING.bash
%doc bash-%{bashv}/AUTHORS bash-%{bashv}/CHANGES bash-%{bashv}/COMPAT
%doc bash-%{bashv}/COPYING bash-%{bashv}/ChangeLog bash-%{bashv}/NEWS
%doc bash-%{bashv}/RBASH
%doc bash-%{bashv}/doc/README bash-%{bashv}/doc/FAQ bash-%{bashv}/doc/INTRO
%doc bash-%{bashv}/doc/bash.html bash-%{bashv}/doc/bashref.html
%doc bash-%{bashv}/doc/bash.pdf bash-%{bashv}/doc/bashref.pdf
%doc bash-completion

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/bash
%attr(0644,root,root) %{_includedir}/bash/*.h
%attr(0755,root,root) %dir %{_includedir}/bash/builtins
%attr(0644,root,root) %{_includedir}/bash/builtins/*.h
%attr(0755,root,root) %dir %{_includedir}/bash/include
%attr(0644,root,root) %{_includedir}/bash/include/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/%{name}.pc
%dir %{_datadir}/cmake
%dir %{_datadir}/cmake/bash-completion
%attr(0644,root,root) %{_datadir}/cmake/bash-completion/*.cmake
%attr(0644,root,root) %{_datadir}/pkgconfig/bash-completion.pc
# otro
%license COPYING.bash-completion COPYING.bash
%doc bash-%{bashv}/AUTHORS bash-%{bashv}/CHANGES bash-%{bashv}/COMPAT
%doc bash-%{bashv}/COPYING bash-%{bashv}/ChangeLog bash-%{bashv}/NEWS
%doc bash-%{bashv}/RBASH
%doc bash-%{bashv}/doc/README bash-%{bashv}/doc/FAQ bash-%{bashv}/doc/INTRO
%doc bash-%{bashv}/doc/bash.html bash-%{bashv}/doc/bashref.html
%doc bash-%{bashv}/doc/bash.pdf bash-%{bashv}/doc/bashref.pdf
%doc bash-completion


%changelog
* Fri May 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc5
- Add bash-completion package

* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc4
- Use insinfo macro, add post/preun requires.

* Mon Apr 03 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc3
- Add legacy python2 path support

* Sat Mar 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc2
- Initial build for LFS 11.3 environment.
