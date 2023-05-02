%if 0%{!?__sed:1} == 1
%global __sed %{_bindir}/sed
%endif

Name:     nspr
Version:  4.35
Release:  %{?repo}0.rc1%{?dist}
Summary:  API for system level and libc-like functions

Group:    System Environment/Libraries
License:  MPL-2.0
URL:      https://firefox-source-docs.mozilla.org/nspr/index.html
Source0:  https://archive.mozilla.org/pub/nspr/releases/v%{version}/src/nspr-%{version}.tar.gz

BuildRequires:  %__sed
#Requires:	

%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API for
system level and libc-like functions. The API is used in the Mozilla
clients, many of Red Hat's and Oracle's server applications, and other
software offerings.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against the nspr libraries.

%prep
%setup -q
cd nspr
%__sed -ri '/^RELEASE/s/^/#/' pr/src/misc/Makefile.in
%__sed -i 's#$(LIBRARY) ##'   config/rules.mk


%build
cd nspr
%configure --prefix=%{_prefix}     \
  --includedir=%{_includedir}/nspr \
  --with-mozilla                   \
%if "%{_arch}" == "x86_64"
  --with-pthreads --enable-64bit
%else
  --with-pthreads
%endif
make %{?_smp_mflags}


%install
cd nspr
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libnspr4.so
%attr(0755,root,root) %{_libdir}/libplc4.so
%attr(0755,root,root) %{_libdir}/libplds4.so
%license nspr/LICENSE
%doc nspr/LICENSE

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/nspr-config
%dir %{_includedir}/nspr
%attr(0644,root,root) %{_includedir}/nspr/*.h
%dir %{_includedir}/nspr/md
%attr(0644,root,root) %{_includedir}/nspr/md/*.cfg
%dir %{_includedir}/nspr/obsolete
%attr(0644,root,root) %{_includedir}/nspr/obsolete/*.h
%dir %{_includedir}/nspr/private
%attr(0644,root,root) %{_includedir}/nspr/private/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/nspr.pc
%attr(0644,root,root) %{_datadir}/aclocal/nspr.m4
%license nspr/LICENSE
%doc nspr/LICENSE




%changelog
* Tue May 2 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.35-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
