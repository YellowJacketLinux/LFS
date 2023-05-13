# NOTE - daemon init scripts not yet installed

# TODO - rrsync ?? Requires python3-braceexpand

%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
%global nodoxygen foo
%endif
%endif

%if 0%{?!nodoxygen:1} == 1
%if 0%{?!__doxygen:1} == 1
%global __doxygen %{_bindir}/doxygen
%endif
%endif

Name:     rsync
Version:  3.2.7
Release:  %{?repo}0.rc1%{?dist}
Summary:  fast incremental file transfer

Group:    System Environment/Utilities
License:  GPL-3.0-or-later with exception
URL:      https://rsync.samba.org/
Source0:  https://download.samba.org/pub/rsync/src/rsync-3.2.7.tar.gz

BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(libzstd)
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
%if 0%{?!nodoxygen:1} == 1
BuildRequires:  %{__doxygen}
%endif
Requires: openssh-clients

%description
Rsync is a fast and extraordinarily versatile file copying tool for
both remote and local files.

Rsync uses a delta-transfer algorithm which provides a very fast method
for bringing remote files into sync.  It does this by sending just the
differences in the files across the link, without requiring that both
sets of files are present at one of the ends of the link beforehand.

%package -n rsyncd
Group:    Daemons/Network
Summary:  Support for the rsyncd daemon
BuildArch:  noarch
Requires: %{name} = %{version}-%{release}

%description -n rsyncd
This package provides the necessary support to run rsync as a daemon.

%prep
%setup -q


%build
%configure \
  --disable-lz4 \
  --disable-xxhash \
  --without-included-zlib
make %{?_smp_mflags}
%if 0%{?!nodoxygen:1} == 1
%{__doxygen}
%endif

%install
make install DESTDIR=%{buildroot}
%if 0%{?!nodoxygen:1} == 1
mv dox/html api-html
%endif
[ ! -d %{buildroot}%{_sysconfdir}/ ] && \
  mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/rsyncd.conf << "EOF"
# This is a basic rsync configuration file
# It exports a single module without user authentication.

motd file = /srv/rsync/welcome.msg
use chroot = yes

[localhost]
    path = /srv/rsync
    comment = Default rsync module
    read only = yes
    list = yes
    uid = rsyncd
    gid = rsyncd

EOF

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/rsync
%attr(0755,root,root) %{_bindir}/rsync-ssl
%attr(0644,root,root) %{_mandir}/man1/rsync.1*
%attr(0644,root,root) %{_mandir}/man1/rsync-ssl.1*
%license COPYING
%doc COPYING NEWS.md SECURITY.md TODO 
%doc rsync.1.html rsync-ssl.1.html
%doc rsync.1.md rsync-ssl.1.md
%if 0%{?!nodoxygen:1} == 1
%doc api-html
%endif

%files -n rsyncd
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/rsyncd.conf
%attr(0644,root,root) %{_mandir}/man5/rsyncd.conf.5*
%attr(0750,rsyncd,rsyncd) %dir /srv/rsync
%license COPYING
%doc COPYING rsyncd.conf.5.html rsyncd.conf.5.md

%changelog
* Sat May 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.2.7-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
