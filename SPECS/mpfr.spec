# TODO - this may belong in /lib and not /usr/lib

# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     mpfr
Version:  4.2.0
Release:  %{?repo}0.rc2%{?dist}
Summary:  Library for multiple-precision floating-point computations

Group:    System Environment/Libraries
License:  LGPLv3
URL:      https://www.mpfr.org/
Source0:  https://ftp.gnu.org/gnu/mpfr/%{name}-%{version}.tar.xz

BuildRequires:	gmp-devel

%description
The MPFR library is a C library for multiple-precision floating-point
computations with correct rounding.

%package devel
Summary:  Developer files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the files necessary to compile software that
links against the %{name} library.

%prep
%setup -q
# Fix a test case based on a bug of old Glibc releases
sed -e 's/+01,234,567/+1,234,567 /' \
    -e 's/13.10Pd/13Pd/'            \
    -i tests/tsprintf.c

%build
%configure         \
  --disable-static \
  --enable-thread-safe
make %{?_smp_mflags}
make html

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/mpfr

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libmpfr.so.6.2.0
%{_libdir}/libmpfr.so.6
%license COPYING COPYING.LESSER
%doc %{name}-make.check.log
%doc AUTHORS BUGS COPYING COPYING.LESSER NEWS TODO

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libmpfr.so
%attr(0644,root,root) %{_libdir}/pkgconfig/mpfr.pc
%attr(0644,root,root) %{_infodir}/mpfr.info*
%exclude %{_infodir}/dir
%doc examples doc/FAQ.html doc/mpfr.html


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.2.0-0.rc2
- tabs to spaces, use %%insinfo macro

* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.2.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
