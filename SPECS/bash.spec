# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:		bash
Version:	5.2.15
Release:	%{?repo}0.rc4%{?dist}
Summary:	The Bourne Again Shell

Group:		System Environment/Shells
License:	GPLv3
URL:		https://gnu.org/software/bash
Source0:	https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
# These are from BLFS - https://www.linuxfromscratch.org/blfs/view/stable/postlfs/profile.html 2023-03-11
Source1:	bash-profile
Source2:	bash-bashrc

BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
Requires(post):	%{insinfo}
Requires(preun):	%{insinfo}

%description
Bash is a Unix shell and scripting language developed for the GNU project as a
replacement for the Bourne shell. Bash is the stanard shell for the GNU/Linux
operating system.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the headers and related files needed to build software
that uses bash.

%prep
%setup -q


%build
%configure \
  --bindir=/bin \
  --without-bash-malloc \
  --with-installed-readline 
#  --docdir=%{_datadir}/doc/%{name}-%{version}
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
%find_lang %{name}
ln -sf bash %{buildroot}/bin/sh
install -m644 -D %{SOURCE1} %{buildroot}/%{_sysconfdir}/profile
install -m644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/bashrc
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
%license COPYING
%doc AUTHORS CHANGES COMPAT COPYING ChangeLog NEWS RBASH
%doc doc/README doc/FAQ doc/INTRO doc/bash.html doc/bashref.html
%doc doc/bash.pdf doc/bashref.pdf

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/bash
%attr(0644,root,root) %{_includedir}/bash/*.h
%attr(0755,root,root) %dir %{_includedir}/bash/builtins
%attr(0644,root,root) %{_includedir}/bash/builtins/*.h
%attr(0755,root,root) %dir %{_includedir}/bash/include
%attr(0644,root,root) %{_includedir}/bash/include/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/%{name}.pc
%license COPYING



%changelog
* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc4
- Use insinfo macro, add post/preun requires.

* Mon Apr 03 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc3
- Add legacy python2 path support

* Sat Mar 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.15-0.rc2
- Initial build for LFS 11.3 environment.
