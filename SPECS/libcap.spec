Name:		libcap
# NOTE - 2.68 is out, 03/28/2023
Version:	2.67
Release:	%{?repo}0.rc1%{?dist}
Summary:	POSIX.1e implenentation library

Group:		System Environment/Libraries
License:	BSD 3-clause and GPLv2
URL:		https://sites.google.com/site/fullycapable/
Source0:	https://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz

BuildRequires:	libattr-devel

%description
Libcap is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package utilities
Group:		System Administration/Utilities
Summary:	libcap utilities
Requires:	%{name} = %{version}-%{release}

%description utilities
This package includes the libcap system administration utilities.

%package devel
Group:		Development/Libraries
Summary:	Development files for libcap
Requires:	%{name} = %{version}-%{release}

%description devel
This package includes the developer files needed to compile software
that links against the libcap libraries.

%prep
%setup -q


%build
sed -i '/install -m.*STA/d' libcap/Makefile
make %{?_smp_mflags} prefix=%{_prefix} lib=%{_lib}

%check
make test > %{name}-make.test.log 2>&1

%install
make prefix=%{_prefix} lib=%{_lib} DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libcap.so.2.67
%attr(0755,root,root) %{_libdir}/libpsx.so.2.67
%{_libdir}/libcap.so.2
%{_libdir}/libpsx.so.2
%license License
%doc README License %{name}-make.test.log

%files utilities
%defattr(-,root,root,-)
%attr(0755,root,root) %{_sbindir}/capsh
%attr(0755,root,root) %{_sbindir}/getcap
%attr(0755,root,root) %{_sbindir}/getpcaps
%attr(0755,root,root) %{_sbindir}/setcap
%attr(0644,root,root) %{_mandir}/man1/capsh.1*
%attr(0644,root,root) %{_mandir}/man8/captree.8*
%attr(0644,root,root) %{_mandir}/man8/getcap.8*
%attr(0644,root,root) %{_mandir}/man8/getpcaps.8*
%attr(0644,root,root) %{_mandir}/man8/setcap.8*
%license License

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/sys/capability.h
%attr(0644,root,root) %{_includedir}/sys/psx_syscall.h
%{_libdir}/libcap.so
%{_libdir}/libpsx.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libcap.pc
%attr(0644,root,root) %{_libdir}/pkgconfig/libpsx.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*

%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.67-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
