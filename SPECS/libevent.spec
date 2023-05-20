%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
%global nodoxygen foo
%endif
%endif

Name:     libevent
Version:  2.1.12
Release:  %{?repo}0.rc1%{?dist}
Summary:  An event notification library

Group:    System Environment/Libraries
License:  BSD-3-Clause
URL:      https://libevent.org/
Source0:  https://github.com/libevent/libevent/releases/download/release-%{version}-stable/libevent-%{version}-stable.tar.gz
# see https://github.com/libevent/libevent/pull/1227/files
Patch0:   libevent-2.1.12-libressl.patch
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
%if 0%{!?nodoxygen:1} == 1
BuildRequires:  doxygen
%endif
#Requires:	

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. Furthermore, libevent also support callbacks due to
signals or regular timeouts.

libevent is meant to replace the event loop found in event driven network
servers. An application just needs to call event_dispatch() and then
add or remove events dynamically without having to change the event loop. 

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against %{name}.

%prep
%setup -n %{name}-%{version}-stable
%patch 0 -p1
%__sed -i 's/python/&3/' event_rpcgen.py


%build
%configure --disable-static
make %{?_smp_mflags}
%if 0%{!?nodoxygen:1} == 1
doxygen Doxyfile
%endif

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
%if 0%{!?nodoxygen:1} == 1
mkdir -p rpmdoc/api
cp -v -R doxygen/html/* rpmdoc/api/
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libevent-2.1.so.7.0.1
%{_libdir}/libevent-2.1.so.7
%attr(0755,root,root) %{_libdir}/libevent_core-2.1.so.7.0.1
%{_libdir}/libevent_core-2.1.so.7
%attr(0755,root,root) %{_libdir}/libevent_extra-2.1.so.7.0.1
%{_libdir}/libevent_extra-2.1.so.7
%attr(0755,root,root) %{_libdir}/libevent_openssl-2.1.so.7.0.1
%{_libdir}/libevent_openssl-2.1.so.7
%attr(0755,root,root) %{_libdir}/libevent_pthreads-2.1.so.7.0.1
%{_libdir}/libevent_pthreads-2.1.so.7
%license LICENSE
%doc ChangeLog* LICENSE README.md
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/event_rpcgen.py
%dir %{_includedir}/event2
%attr(0644,root,root) %{_includedir}/event2/*.h
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent_core.so
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license LICENSE
%doc ChangeLog* LICENSE README.md sample
%if 0%{!?nodoxygen:1} == 1
%doc rpmdoc/api
%endif

%changelog
* Thu Apr 27 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.1.12-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
