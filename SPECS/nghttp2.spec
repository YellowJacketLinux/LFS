# needs work for 1.cli. repo

Name:     nghttp2
Version:  1.52.0
Release:	%{?repo}0.rc1%{?dist}
Summary:  HTTP/2 C Library

Group:    System Environment/Libraries
License:  MIT
URL:      https://nghttp2.org/
Source0:  https://github.com/nghttp2/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz

#BuildRequires:  libxml2-devel
BuildRequires:  python3-devel
#Requires:	

%description
nghttp2 is an implementation of HTTP/2 and its header compression
algorithm HPACK in C.

The framing layer of HTTP/2 is implemented as a form of reusable C
library. On top of that, we have implemented HTTP/2 client, server and
proxy. We have also developed load test and benchmarking tool for HTTP/2.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package provides the files needed to compile software that links
against the %{name} library.

%prep
%setup -q


%build
PYTHON=%{python3} \
%configure \
  --with-libxml2 \
  --disable-static
# \
#  --enable-lib-only
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/nghttp2

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libnghttp2.so.14.24.1
%{_libdir}/libnghttp2.so.14
%attr(0644,root,root) %{_mandir}/man1/*.1*
%dir %{_datadir}/nghttp2
%attr(0755,root,root) %{_datadir}/nghttp2/fetch-ocsp-response
%license COPYING
%doc AUTHORS COPYING ChangeLog README.rst

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/nghttp2
%attr(0644,root,root) %{_includedir}/nghttp2/*.h
%{_libdir}/libnghttp2.so
%{_libdir}/pkgconfig/libnghttp2.pc
%license COPYING
%doc AUTHORS COPYING ChangeLog README.rst examples


%changelog
* Wed Apr 26 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.52.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
