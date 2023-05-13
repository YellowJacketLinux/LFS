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

%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed
%endif

Name:     popt
Version:  1.19
Release:	%{?repo}0.rc1%{?dist}
Summary:  command line option parsing library

Group:    System Environment/Libraries
License:  MIT
URL:      https://github.com/rpm-software-management/popt
Source0:  https://ftp.osuosl.org/pub/rpm/popt/releases/popt-1.x/popt-%{version}.tar.gz

%if 0%{?!nodoxygen:1} == 1
BuildRequires:  %{__doxygen}
BuildRequires:  %{__sed}
%endif

%description
This is the popt(3) command line option parsing library. While it is
similar to getopt(3), it contains a number of enhancements, including:

1) popt is fully reentrant
2) popt can parse arbitrary argv[] style arrays while 
getopt(3) makes this quite difficult
3) popt allows users to alias command line arguments
4) popt provides convenience functions for parsing strings
into argv[] style arrays

%package devel
Group:    Development/Libraries
Summary:  Development files for the popt library
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against the popt library.


%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}
%if 0%{?!nodoxygen:1} == 1
%__sed -i 's@\./@src/@' Doxyfile
%{__doxygen}
%endif

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
%{find_lang} popt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f popt.lang
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/libpopt.so.0.0.2
%{_libdir}/libpopt.so.0
%license COPYING
%doc COPYING CREDITS README
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/popt.h
%{_libdir}/libpopt.so
%attr(0644,root,root) %{_libdir}/pkgconfig/popt.pc
%attr(0644,root,root) %{_mandir}/man3/popt.3.*
%license COPYING
%doc COPYING CREDITS README
%if 0%{?!nodoxygen:1} == 1
%doc doxygen/html
%endif

%changelog
* Sat May 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.19-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
