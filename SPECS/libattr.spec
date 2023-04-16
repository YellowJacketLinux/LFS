%define tarname attr
Name:     libattr
Version:  2.5.1
Release:  %{?repo}0.rc2%{?dist}
Summary:  Extended File System Attribute Library

Group:    System Environment/Libraries
License:  LGPLv2.1 and GPLv2
URL:      https://savannah.nongnu.org/projects/attr
Source0:  https://download.savannah.gnu.org/releases/attr/%{tarname}-%{version}.tar.gz

#BuildRequires:	
#Requires:	

%description
This package contains a library for working with file system extended
attributes.

%package devel
Summary:  Developer files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and other files needed to compile
software that links against the %{name} library.

%package utils
Summary:  Utilities for managing extended attributes
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}
Provides: %{tarname} = %{version}

%description utils
This package provides the attr, getfattr, and setfattry command line
utilities for working with extended file system attributes.

%prep
%setup -n %{tarname}-%{version}

%build
%configure --libdir=/%{_lib} --disable-static
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot} pkgconfdir=%{_libdir}/pkgconfig
%find_lang attr
rm -rf %{buildroot}%{_datadir}/doc/attr
sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}%{_libdir}/pkgconfig/libattr.pc
rm -f %{buildroot}/%{_lib}/libattr.so
ln -sf ../../%{_lib}/libattr.so.1.1.2501 %{buildroot}%{_libdir}/libattr.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f attr.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/libattr.so.1.1.2501
/%{_lib}/libattr.so.1
%license doc/COPYING doc/COPYING.LGPL
%doc %{name}-make.check.log
%doc README doc/CHANGES doc/COPYING doc/COPYING.LGPL doc/PORTING

%files devel
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
%license doc/COPYING doc/COPYING.LGPL
%doc examples

%files utils
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/xattr.conf
%attr(0755,root,root) %{_bindir}/attr
%attr(0755,root,root) %{_bindir}/getfattr
%attr(0755,root,root) %{_bindir}/setfattr
%attr(0644,root,root) %{_mandir}/man1/attr.1*
%attr(0644,root,root) %{_mandir}/man1/getfattr.1*
%attr(0644,root,root) %{_mandir}/man1/setfattr.1*

%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.5.1-0.rc2
- Spec file cleanup, rebuild with newly packaged gcc

* Wed Mar 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.5.1-0.rc1
- Initial spec file for YJL (LFS 11.3 environment)
