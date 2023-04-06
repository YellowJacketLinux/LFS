Name:		acl
Version:	2.3.1
Release:	%{?repo}0.rc1%{?dist}
Summary:	POSIX Access Control List tools

Group:		System Environment/Utilities
License:	GPLv2 and LGPLv2.1
URL:		https://savannah.nongnu.org/projects/acl/
Source0:	https://download.savannah.gnu.org/releases/acl/%{name}-%{version}.tar.xz

BuildRequires:	coreutils libattr-devel
Requires:	libacl = %{version}-%{release}

%description
This package contains tools for manipulating POSIX Access Control
Lists.

%package -n libacl
Group:		System Environment/Libraries
Summary:	The libacl shared library

%description -n libacl
This package includes the libacl shared library.

%package -n libacl-devel
Group:		Development/Libraries
Summary:	libacl development files
Requires:	libacl = %{version}-%{release}

%description -n libacl-devel
This package contains the files needed to compile software that links
against the libacl library.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}
rm -rf %{buildroot}%{_datadir}/doc/acl


%post -n libacl -p /sbin/ldconfig
%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/chacl
%attr(0755,root,root) %{_bindir}/getfacl
%attr(0755,root,root) %{_bindir}/setfacl
%attr(0644,root,root) %{_mandir}/man1/chacl.1*
%attr(0644,root,root) %{_mandir}/man1/getfacl.1*
%attr(0644,root,root) %{_mandir}/man1/setfacl.1*
%attr(0644,root,root) %{_mandir}/man5/acl.5*
%license doc/COPYING doc/COPYING.LGPL
%doc %{name}-make.check.log
%doc doc/CHANGES doc/COPYING

%files -n libacl
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libacl.so.1.1.2301
%{_libdir}/libacl.so.1
%license doc/COPYING doc/COPYING.LGPL

%files -n libacl-devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/acl
%attr(0644,root,root) %{_includedir}/acl/libacl.h
%attr(0644,root,root) %{_includedir}/sys/acl.h
%{_libdir}/libacl.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libacl.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*
%doc doc/libacl.txt doc/extensions.txt



%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.3.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
