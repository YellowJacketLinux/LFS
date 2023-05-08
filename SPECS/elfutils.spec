%global slibv 0.188
%global compatname 0_188

Name:     elfutils
Version:  0.188
Release:  %{?repo}0.rc4%{?dist}
Summary:  elfutils

Group:    System Environment/Base
License:  GPLv3, GPLv2, LGPL-3.0-or-later or GPL-2.0-or-later and GPL-3.0-or-later
URL:      http://elfutils.org/
Source0:  https://sourceware.org/ftp/%{name}/%{version}/%{name}-%{version}.tar.bz2
#Patch0:   elfutils-libcurl.patch

BuildRequires:  zlib-devel
BuildRequires:  libzstd-devel
BuildRequires:  liblzma-devel
BuildRequires:  libbz2-devel
#Requires:	

%description
elfutils is a collection of utilities and libraries to read, create and
modify ELF binary files, find and handle DWARF debug data, symbols,
thread state and stacktraces for processes and core files on GNU/Linux.

%package libs
Summary:  The elfutils shared libraries
Group:    System Enviroment/Libraries
Provides: %{name}-libelf = %{version}
Provides: %{name}-libdw = %{version}
Requires: %{name}-libs-compat-%{compatname} = %{version}-%{release}

%description libs
This package provides the elfutils shared libraries, including the libelf
and libdw libraries.

%package libs-compat-%{compatname}
Summary:  The specific versions of the elfutils shared libraries
Group:    System Environment/Libraries

%description libs-compat-%{compatname}
This package provides specific versions of the elfutils libraries, allowing
elfutils-libs to be updated without breaking applications that link against
these specific versions.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Provides: %{name}-libelf-devel = %{version}
Provides: %{name}-libdw = %{version}


%description devel
This package the headers and other related files needed to compile software
that links against the libelf libraries.


%prep
%setup -q
#%%patch0 -p0


%build
%configure \
  --disable-rpath \
  --disable-debuginfod \
  --enable-libdebuginfod=dummy \
  --program-prefix="eu-"

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build." > %{name}-make.check.log
%endif

%post libs-compat-%{compatname} -p /sbin/ldconfig
%postun libs-compat-%{compatname} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/*
%exclude %{_libdir}/*.a
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man7/*.7*
%exclude %{_sysconfdir}/profile.d/debuginfod.csh
%exclude %{_sysconfdir}/profile.d/debuginfod.sh
%license COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL
%doc COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL
%doc AUTHORS ChangeLog NEWS NOTES README THANKS TODO
%doc %{name}-make.check.log

%files libs
%defattr(-,root,root,-)
%{_libdir}/libasm.so.1
%{_libdir}/libdebuginfod.so.1
%{_libdir}/libdw.so.1
%{_libdir}/libelf.so.1
%license COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL
%doc AUTHORS ChangeLog NEWS NOTES README THANKS TODO
%doc COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL

%files libs-compat-%{compatname}
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libasm-%{slibv}.so
%attr(0755,root,root) %{_libdir}/libdebuginfod-%{slibv}.so
%attr(0755,root,root) %{_libdir}/libdw-%{slibv}.so
%attr(0755,root,root) %{_libdir}/libelf-%{slibv}.so
%license COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL

%files devel
%defattr(-,root,root,-)
%{_libdir}/libasm.so
%{_libdir}/libdebuginfod.so
%{_libdir}/libdw.so
%{_libdir}/libelf.so
%attr(0644,root,root) %{_includedir}/*.h
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_mandir}/man3/*.3*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL
%doc AUTHORS ChangeLog NEWS NOTES README THANKS TODO
%doc COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL

%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.188-0.rc4
- Spec file cleanup

* Thu Mar 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.188-0.rc3
- Create a libs-compat package so elfutils-libs can be updated without breaking
- packages that haven't been rebuilt.

* Tue Mar 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.188-0.rc2
- Use eu- prefix for binaries

* Tue Mar 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.188-0.rc1
- Initial spec file.
