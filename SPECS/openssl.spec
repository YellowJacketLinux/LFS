%if 0%{!?_ssldir:1} == 1
%global _ssldir %{_sysconfdir}/ssl
%endif

Name:     openssl
Version:  3.1.0
Release:  %{?repo}0.rc3%{?dist}
Summary:  cryptography and secure communication toolkit

Group:    System Environment/Libraries
License:  Apache-2.0
URL:      https://www.openssl.org/
Source0:  https://www.openssl.org/source/openssl-%{version}.tar.gz
Source11:  openssl-3.1.0-man1.filelist
Source13:  openssl-3.1.0-man3.filelist
Source17:  openssl-3.1.0-man7.filelist

BuildRequires:  perl
BuildRequires:  zlib-devel
Requires:	%{name}-libs = %{version}-%{release}

%description
OpenSSL is a robust, commercial-grade, full-featured toolkit for general-
purpose cryptography and secure communication.

%package libs
Group:    System Environment/Libraries
Summary:  OpenSSL shared libraries
Requires: make-ca

%description libs
This packages contains the OpenSSL shared libraries.

%package devel
Group:    Development/Libraries
Summary:  OpenSSL developer files
Requires: %{name}-libs = %{version}-%{release}
Conflicts:  libressl-devel

%description devel
This package contains the developer files needed to compile software
that links against the OpenSSL libraries.

%package man7
Group:    Documentation
Summary:  OpenSSL man 7 pages
Requires: %{name}-libs = %{version}-%{release}
BuildArch:  noarch

%description man7
This package contains the OpenSSL man7 pages that *most* users of
YJL probably do not need.

%prep
%setup -q
cp %{SOURCE11} ./man1.filelist
cp %{SOURCE13} ./man3.filelist
cp %{SOURCE17} ./man7.filelist


%build
#%%configure
./config --prefix=%{_prefix}   \
         --openssldir=/etc/ssl \
         --libdir=%{_lib}      \
         shared                \
         no-ssl3               \
         no-dtls               \
         no-weak-ssl-ciphers   \
         zlib-dynamic
make %{?_smp_mflags}


%check
%if 0%{?runtests:1} == 1
make test > %{name}-make.test.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.test.log
%endif


%install
# make MANSUFFIX=ssl install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/openssl


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f man1.filelist
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/c_rehash
%attr(0755,root,root) %{_bindir}/openssl
%attr(0644,root,root) %{_ssldir}/openssl.cnf.dist
%attr(0644,root,root) %config(noreplace) %{_ssldir}/openssl.cnf
%exclude %{_ssldir}/ct_log_list.cnf.dist
%exclude %{_ssldir}/ct_log_list.cnf
%dir %{_ssldir}/misc
%attr(0755,root,root) %{_ssldir}/misc/CA.pl
%attr(0755,root,root) %{_ssldir}/misc/tsget.pl
%{_ssldir}/misc/tsget
%attr(0644,root,root) %{_mandir}/man5/config.5ossl*
%attr(0644,root,root) %{_mandir}/man5/fips_config.5ossl*
%attr(0644,root,root) %{_mandir}/man5/x509v3_config.5ossl*
%license LICENSE.txt
%doc CHANGES.md NEWS.md NOTES-UNIX.md README* LICENSE.txt
%doc %{name}-make.test.log
%doc doc/html/man1
%doc doc/html/man5

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libcrypto.so.3
%attr(0755,root,root) %{_libdir}/libssl.so.3
%dir %{_libdir}/engines-3
%attr(0755,root,root) %{_libdir}/engines-3/*.so
%dir %{_libdir}/ossl-modules
%attr(0755,root,root) %{_libdir}/ossl-modules/legacy.so
%license LICENSE.txt
%doc %{name}-make.test.log
%doc CHANGES.md NEWS.md NOTES-UNIX.md README* LICENSE.txt

%files devel -f man3.filelist
%defattr(-,root,root,-)
%dir %{_includedir}/openssl
%attr(0644,root,root) %{_includedir}/openssl/*.h
%{_libdir}/libcrypto.so
%{_libdir}/libssl.so
%exclude %{_libdir}/libcrypto.a
%exclude %{_libdir}/libssl.a
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license LICENSE.txt
%doc CHANGES.md NEWS.md NOTES-UNIX.md README* LICENSE.txt
%doc doc/html/man3

%files man7 -f man7.filelist
%defattr(-,root,root,-)
%license LICENSE.txt
%doc CHANGES.md NEWS.md NOTES-UNIX.md README* LICENSE.txt
%doc doc/html/man7

%changelog
* Fri May 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.1.0-0.rc3
- Rebuild with gcc 12.3.0

* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.1.0-0.rc2
- Disable SSLv2,SSLv3,DTLS,weak ciphers (I believe disabled by
- default but...)

* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.1.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
