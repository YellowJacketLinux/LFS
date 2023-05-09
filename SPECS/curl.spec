Name:     curl
Version:  8.0.1
Release:  %{?repo}0.rc1%{?dist}
Summary:  Command line utility for retriving files from remote servers

Group:    foo
License:  curl
URL:      https://curl.se/
Source0:  https://curl.se/download/curl-%{version}.tar.xz

BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(hogweed)
BuildRequires:  pkgconfig(libbrotlidec)
BuildRequires:  pkgconfig(libbrotlicommon)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libunistring-devel
BuildRequires:  make-ca
Requires: make-ca
Requires: libcurl = %{version}-%{release}

%description
Curl (also known as cURL) is a command line utility and shared library
for retrieving content from remote servers.

%package -n libcurl
Group:    System Environment/Libraries
Summary:  The curl shared library

%description -n libcurl
This package contains the libcurl shared library.

%package -n libcurl-devel
Group:    Development/Libraries
Summary:  libcurl development files
Requires: libcurl = %{version}-%{release}

%description -n libcurl-devel
This package contains the files needed to build software that links
against the libcurl library.

%prep
%setup -q


%build
%configure \
  --disable-static \
  --with-gnutls \
  --enable-threaded-resolver \
  --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt

make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
# a few tests fail
###
# TESTDONE: 1287 tests out of 1291 reported OK: 99%
#
# TESTFAIL: These test cases failed: 1139 1140 1173 1177
###
make test > %{name}-make.test.log 2>&1 ||:
%else
echo "make test not run at package build" > %{name}-make.test.log
%endif

%install
make install DESTDIR=%{buildroot}

rm -rf docs/examples/.deps
find docs \( -name Makefile\* -o -name \*.1 -o -name \*.3 \) -exec rm {} \;
# docs w/ %doc

%post -n libcurl -p /sbin/ldconfig
%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/curl.1*
%license COPYING
%doc CHANGES COPYING README RELEASE-NOTES 
%doc %{name}-make.test.log

%files -n libcurl
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libcurl.so.4.8.0
%{_libdir}/libcurl.so.4
%license COPYING
%doc CHANGES COPYING README RELEASE-NOTES docs

%files -n libcurl-devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/curl-config
%attr(0644,root,root) %{_datadir}/aclocal/libcurl.m4
%dir %{_includedir}/curl
%attr(0644,root,root) %{_includedir}/curl/*.h
%{_libdir}/libcurl.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libcurl.pc
%attr(0644,root,root) %{_mandir}/man1/curl-config.1*
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license COPYING
%doc CHANGES COPYING README RELEASE-NOTES docs


%changelog
* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 8.0.1-0.rc1
- Update to 8.0.1

* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 7.88.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
