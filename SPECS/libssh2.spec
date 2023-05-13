Name:     libssh2
Version:  1.10.0
Release:	%{?repo}0.rc2%{?dist}
Summary:  C library SSH2 implementation

Group:    System Environment/Libraries
License:  BSD-3-Clause
URL:      https://www.libssh2.org/
Source0:  https://www.libssh2.org/download/libssh2-%{version}.tar.gz
Patch0:   https://www.linuxfromscratch.org/patches/blfs/11.3/libssh2-1.10.0-upstream_fix-1.patch
Patch1:   libssh2-1.10.0-libressl.patch

BuildRequires:  gnupg-devel
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  openssh-server
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
#Requires:	

%description
libssh2 is a client-side C library implementing the SSH2 protocol.

%package devel
Group:    Development/Libraries
Summary:  Development files for libssh2
Requires: %{name} = %{version}-%{release}
%if 0%{?libresslAPI:1} == 1
Requires: libressl-devel
%else
Requires: openssl-devel
%endif

%description devel
This package contains the developer files needed to compile software
that links against the libssh2 library.

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1


%build
%configure --disable-static
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" >> %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libssh2.so.1.0.1
%{_libdir}/libssh2.so.1
%license COPYING
%doc COPYING NEWS README RELEASE-NOTES
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libssh2.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libssh2.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license COPYING
%doc COPYING NEWS README RELEASE-NOTES



%changelog
* Sat May 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.10.0-0.rc2
- Fix build against LibreSSL

* Sat May 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.10.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
