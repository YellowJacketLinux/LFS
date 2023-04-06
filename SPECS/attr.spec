Name:		attr
Version:	2.5.1
Release:	%{?repo}0.rc1%{?dist}
Summary:	Utilities for filesystem extended attributes

Group:		System Environment/Utilities
License:	GPLv2 LGPLv2
URL:		https://savannah.nongnu.org/projects/attr/
Source0:	https://download.savannah.gnu.org/releases/attr/%{name}-%{version}.tar.gz

Requires:	libattr = %{version}-%{release}

%description
Binaries for working with filesystem extended attributes.

%package -n libattr
Group:		System Environment/Libraries
Summary:	The libattr shared library

%description -n libattr
This package contains the libattr shared library.

%package -n libattr-devel
Group:		Development/Libraries
Summary:	Development files for libattr
Requires:	libattr = %{version}-%{release}

%description -n libattr-devel
This package contains the developer files needed to compile software
that links against the libattr library.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/attr
%find_lang %{name}

%post -n libattr -p /sbin/ldconfig
%postun -n libattr -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/xattr.conf
%attr(0755,root,root) %{_bindir}/attr
%attr(0755,root,root) %{_bindir}/getfattr
%attr(0755,root,root) %{_bindir}/setfattr
%attr(0644,root,root) %{_mandir}/man1/attr.1*
%attr(0644,root,root) %{_mandir}/man1/getfattr.1*
%attr(0644,root,root) %{_mandir}/man1/setfattr.1*
%license doc/COPYING doc/COPYING.LGPL
%doc doc/CHANGES doc/COPYING doc/COPYING.LGPL
%doc %{name}-make.check.log

%files -n libattr
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libattr.so.1.1.2501
%{_libdir}/libattr.so.1
%license doc/COPYING doc/COPYING.LGPL

%files -n libattr-devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/attr
%attr(0644,root,root) %{_includedir}/attr/*.h
%{_libdir}/libattr.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libattr.pc
%attr(0644,root,root) %{_mandir}/man3/attr_get.3*
%attr(0644,root,root) %{_mandir}/man3/attr_list.3*
%attr(0644,root,root) %{_mandir}/man3/attr_multi.3*
%attr(0644,root,root) %{_mandir}/man3/attr_remove.3*
%attr(0644,root,root) %{_mandir}/man3/attr_set.3*
%{_mandir}/man3/attr_getf.3*
%{_mandir}/man3/attr_listf.3*
%{_mandir}/man3/attr_multif.3*
%{_mandir}/man3/attr_removef.3*
%{_mandir}/man3/attr_setf.3*

%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.5.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
