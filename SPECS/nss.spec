%global sdirv 3_88_1

%if 0%{!?__chmod:1} == 1
%global __chmod %{_bindir}/chmod
%endif

Name:     nss
Version:  3.88.1
Release:  %{?repo}0.rc1%{?dist}
Summary:  security-enabled client and server libraries

Group:    System Environment/Libraries
License:  MPL-2.0
URL:      https://firefox-source-docs.mozilla.org/security/nss/index.html
Source0:  https://archive.mozilla.org/pub/security/nss/releases/NSS_%{sdirv}_RTM/src/nss-%{version}.tar.gz
#Patch0:   https://www.linuxfromscratch.org/patches/blfs/11.3/nss-3.88.1-standalone-1.patch
Patch0:   nss-3.88.1-standalone-rpm.patch

# gyp ??
#BuildRequires:  ninja
BuildRequires:  nspr-devel
BuildRequires:  sqlite3-devel
BuildRequires:  zlib-devel
BuildRequires:  %__chmod
Requires: p11-kit

%description
Network Security Services (NSS) is a set of libraries designed to
support cross-platform development of security-enabled client and server
applications. Applications built with NSS can support SSL v3, TLS,
PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3 certificates,
and other security standards.

%package devel
Group:    Development/Libraries
Summary:  Development files for nss
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that uses the nss libraries.

%package utils
Group:    System Environment/Utilities
Summary:  NSS utilities
Requires: %{name} = %{version}-%{release}

%description utils
This package contains the NSS certutil and pk12util utilities.

%prep
%setup -q
%patch 0 -p1

%build
cd nss

make %{?_smp_mflags} BUILD_OPT=1       \
  NSPR_INCLUDE_DIR=%{_includedir}/nspr \
  USE_SYSTEM_ZLIB=1                    \
  ZLIB_LIBS=-lz                        \
  NSS_ENABLE_WERROR=0                  \
%if "%{_arch}" == "x86_64"
  USE_64=1                             \
%endif
%if 0%{!?runtests:1} == 1
  NSS_DISABLE_GTESTS=1                 \
%endif
  NSS_USE_SYSTEM_SQLITE=1

%check
%if 0%{?runtests:1} == 1
cd nss/tests
HOST=localhost DOMSUF=localdomain ./all.sh ||:
%endif
# results at  ../../test_results/security/localhost.1/results.html 

%install
cd dist

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_libdir}/pkgconfig
install -d -m755 %{buildroot}%{_includedir}/nss

install -m755 Linux*/lib/*.so %{buildroot}%{_libdir}
# below provided by make-ca
rm -f %{buildroot}%{_libdir}/libnssckbi.so
install -m644 Linux*/lib/{*.chk,libcrmf.a} %{buildroot}%{_libdir}
cp -RL {public,private}/nss/* %{buildroot}%{_includedir}/nss
%__chmod 644 %{buildroot}%{_includedir}/nss/*
install -m755 Linux*/bin/{certutil,nss-config,pk12util} \
  %{buildroot}%{_bindir}
install -m644 Linux*/lib/pkgconfig/nss.pc %{buildroot}%{_libdir}/pkgconfig

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/*.so
# these might actually belong in devel ???
%attr(0644,root,root) %{_libdir}/*.chk
%license nss/COPYING nss/trademarks.txt
%doc nss/COPYING nss/trademarks.txt nss/readme.md
%if 0%{?runtests:1} == 1
%doc tests_results/security/localhost.1/results.html
%endif

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/nss-config
%dir %{_includedir}/nss
%attr(0644,root,root) %{_includedir}/nss/*.h
%attr(0644,root,root) %{_includedir}/nss/nssck.api
%attr(0644,root,root) %{_includedir}/nss/templates.c
%attr(0644,root,root) %{_libdir}/libcrmf.a
%{_libdir}/pkgconfig/nss.pc
%license nss/COPYING nss/trademarks.txt
%doc nss/COPYING nss/trademarks.txt nss/readme.md

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/certutil
%attr(0755,root,root) %{_bindir}/pk12util
%license nss/COPYING nss/trademarks.txt
%doc nss/COPYING nss/trademarks.txt nss/readme.md

%changelog

