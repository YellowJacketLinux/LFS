%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

%if 0%{?!__gawk:1} == 1
%global __gawk %{_bindir}/gawk
%endif

Name:     check
Version:  0.15.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  Unit testing framework for C

Group:    Development/Utilities
License:  LGPL-2.1-or-later
URL:      https://libcheck.github.io/check/
Source0:  https://github.com/libcheck/check/releases/download/%{name}/check-%{version}.tar.gz

BuildRequires:  %{__gawk}
Requires: %{__gawk}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
Check is a unit testing framework for C. It features a simple interface
for defining unit tests, putting little in the way of the developer.
Tests are run in a separate address space, so both assertion failures
and code errors that cause segmentation faults or other signals can be
caught. Test results are reportable in the following: Subunit, TAP,
XML, and a generic logging format.

%package devel
Group:    Development/Libraries
Summary:  Development files for libcheck
Requires: check = %{version}-%{release}

%description devel
This package contains the development files needed to compile software
that uses the libcheck library.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/check

%post
/sbin/ldconfig
%{insinfo} %{_infodir}/check.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/check.info %{_infodir}/dir ||:
fi

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/checkmk
%attr(0755,root,root) %{_libdir}/libcheck.so.0.0.0
%{_libdir}/libcheck.so.0
%attr(0644,root,root) %{_infodir}/check.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/checkmk.1*
%license COPYING.LESSER
%doc AUTHORS COPYING.LESSER ChangeLog NEWS README THANKS TODO
%doc doc/example
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/check.h
%attr(0644,root,root) %{_includedir}/check_stdint.h
%exclude %{_libdir}/libcheck.a
%{_libdir}/libcheck.so
%attr(0644,root,root) %{_libdir}/pkgconfig/check.pc
%attr(0644,root,root) %{_datadir}/aclocal/check.m4
%license COPYING.LESSER


%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.15.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
