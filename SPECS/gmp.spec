# TODO - this may belong in /lib and not /usr/lib

# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     gmp
Version:  6.2.1
Release:  %{?repo}0.rc3%{?dist}%{?cpuoptimize}
Summary:  Library for arbitrary precision arithmetic

Group:    System Environment/Libraries
License:  GPLv2/GPLv3 and LGPLv3
URL:      https://gmplib.org/
Source0:  https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz

BuildRequires:  libstdc++-devel

%description
GMP is a free library for arbitrary precision arithmetic, operating on
signed integers, rational numbers, and floating-point numbers. There
is no practical limit to the precision except the ones implied by the
available memory in the machine GMP runs on. GMP has a rich set of
functions, and the functions have a regular interface.

The main target applications for GMP are cryptography applications and
research, Internet security applications, algebra systems, computational
algebra research, etc. 

%package devel
Summary:  Development files for GMP
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the files necessary to compile software that
links against the GMP library.

%prep
%setup -q
%if 0%{!?cpuoptimize:1} == 1
cp configfsf.guess config.guess
cp configfsf.sub config.sub
%endif


%build
%configure     \
  --enable-cxx \
  --disable-static
make %{?_smp_mflags}
make html

%install
make install DESTDIR=%{buildroot}

%check
make check > %{name}-make.check.log 2>&1

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
%attr(0755,root,root) %{_libdir}/libgmp.so.10.4.1
%attr(0755,root,root) %{_libdir}/libgmpxx.so.4.6.1
%{_libdir}/libgmp.so.10
%{_libdir}/libgmpxx.so.4
%license COPYING*
%doc %{name}-make.check.log
%doc AUTHORS COPYING* ChangeLog NEWS README

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%{_infodir}/gmp.info*
%exclude %{_infodir}/dir
%doc doc/gmp.html


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.1-0.rc3
- Tabs to spaces, support optiobal %%cpuoptimize macro.

* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.1-0.rc2
- Scriptlets for the gmp info file

* Wed Apr 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
