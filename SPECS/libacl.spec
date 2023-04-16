%define tarname acl
Name:     lib%{tarname}
Version:  2.3.1
Release:  %{?repo}0.rc2%{?dist}
Summary:  Commands for Manipulating POSIX Access Control Lists

Group:    System Environment/Libraries
License:  LGPLv2.1 and GPLv2
URL:      http://savannah.nongnu.org/projects/acl
Source0:  https://download.savannah.gnu.org/releases/acl/%{tarname}-%{version}.tar.xz

BuildRequires:  libattr-devel
#Requires:	

%description
A library for implementing Posix 1003.1e DS17 Access Control Lists.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and related developer files
needed to compile software that links against the libacl library.

%package utils
Summary:  Command line utilities for working with ACLs
Group:    System Environment/Administration
Requires: %{name} = %{version}-%{release}
Provides: %{tarname} = %{version}

%description utils
This package provides the chacl, getfacl, and setfacl command line
utilities for working with Access Control Lists.

%prep
%setup -n %{tarname}-%{version}

%build
%configure --libdir=/%{_lib} \
           --disable-static
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot} pkgconfdir=%{_libdir}/pkgconfig
%find_lang acl
rm -rf %{buildroot}%{_datadir}/doc/acl

sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}%{_libdir}/pkgconfig/libacl.pc
rm -f %{buildroot}/%{_lib}/libacl.so
ln -sf ../../%{_lib}/libacl.so.1.1.2301 %{buildroot}%{_libdir}/libacl.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f acl.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/libacl.so.1.1.2301
/%{_lib}/libacl.so.1
%license doc/COPYING doc/COPYING.LGPL
%doc README doc/CHANGES doc/COPYING doc/COPYING.LGPL
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/acl
%attr(0644,root,root) %{_includedir}/acl/libacl.h
%attr(0644,root,root) %{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libacl.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license doc/COPYING doc/COPYING.LGPL
%doc doc/extensions.txt doc/libacl.txt

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/*
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man5/*.5*
%license doc/COPYING doc/COPYING.LGPL


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.3.1-0.rc2
- spec file cleanup, rebuild with newly packaged gcc

* Wed Mar 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.3.1-0.rc1
- Initial packaging for YJL (LFS 11.3)
