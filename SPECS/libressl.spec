%if 0%{!?_ssldir:1} == 1
%global _ssldir %{_sysconfdir}/ssl
%endif
%if 0%{!?_pkitls:1} == 1
%global _pkitls %{_sysconfdir}/pki/tls
%endif

%if 0%{!?__sed:1} == 1
%global __sed %{_bindir}/sed
%endif
%if 0%{!?__chrpath:1} == 1
%global __chrpath %{_bindir}/chrpath
%endif

# Shared library versions
%global slibcryptov 50.0.2
%global slibsslv 53.0.2
%global slibtlsv 26.0.2

Name:     libressl
Version:  3.7.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  OpenBSD fork of the OpenSSL Cryptography Suite

Group:    System Environment/Libraries
License:  OpenSSL
URL:      https://www.libressl.org/
Source0:  https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/%{name}-%{version}.tar.gz
Source1:  libressl-yjl-additions.cnf
# some DH params
#  2048
Source20: https://bettercrypto.org/static/dhparams/group14.pem
#  3072
Source21: https://bettercrypto.org/static/dhparams/group15.pem
#  4096
Source22: https://bettercrypto.org/static/dhparams/group16.pem
#  6144
Source23: https://bettercrypto.org/static/dhparams/group17.pem
#  8192
Source24: https://bettercrypto.org/static/dhparams/group18.pem
#  DHE README
Source25: README.DHE.md
###### YJL patches
Patch90:  libressl-3.7.2-cnf-name.patch
Patch91:  libressl-3.7.2-manpage.patch


#BuildRequires:	%%{__chrpath}
BuildRequires:  %{__sed}
Requires: %{name}-libs = %{version}-%{release}

%description
LibreSSL is a fork of OpenSSL 1.0.1g developed by the OpenBSD project.
Our goal is to modernize the codebase, improve security, and apply best
practice development processes from OpenBSD.

%package libs
Summary:  Shared Libraries for LibreSSL
Group:    System Environment/Libraries
Requires: make-ca
#Requires:	ca-certificates

%description libs
This package provides the shared libraries for LibreSSL.

LibreSSL is API compatible with OpenSSL 1.0.1, but does not yet include
all new APIs from OpenSSL 1.0.2 and later. LibreSSL also includes APIs
not yet present in OpenSSL. The current common API subset is OpenSSL
1.0.1.

LibreSSL it is not ABI compatible with any release of OpenSSL, or
necessarily earlier releases of LibreSSL. You will need to relink your
programs to LibreSSL in order to use it, just as in moving between major
versions of OpenSSL.

LibreSSL's installed library version numbers are incremented to account
for ABI and API changes.

%package devel
Summary:  Developer files for LibreSSL
Group:    Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Conflicts:  openssl-devel

%description devel
This package provides the development header files for LibreSSL.

%package dhe-cron
Summary:  Cron scripts to generate DHE groups
Group:    System Administration/Miscellaneous
Requires: %{name} = %{version}-%{release}
Requires: fcron

%description dhe-cron
For servers that support TLS with the DHE key exchange, it is generally
a good idea to generate fresh DHE groups periodically. This package
installs cron job scripts that do so.

For non-servers, all these scripts do is waste CPU cycles. Desktop
users should not install this package.

%prep
%setup -q
%patch 90 -p1
%patch 91 -p1
# These aren't renamed in the patches to reduce patch size.
mv openssl.cnf libressl.cnf
mv man/openssl.cnf.5 man/libressl.cnf.5
mv apps/openssl/openssl.1 apps/openssl/libressl.1

cp %{SOURCE25} .


%build
%configure \
  --with-openssldir=%{_ssldir} \
  --libdir=/%{_lib} 

# fails biotest w/ this option
#  --enable-extratests

##%% from RHEL/CentOS OpenSSL spec file ##%%
# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
  
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.check.log
%endif


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_ssldir}/cert.pem
install -d %{buildroot}%{_ssldir}/csr
#install -d %%{buildroot}%%{_sysconfdir}/ssl
#ln -s ../pki/tls/libressl.cnf %%{buildroot}%%{_sysconfdir}/ssl/libressl.cnf
install -d %{buildroot}%{_pkitls}

#rename openssl binary
mv %{buildroot}%{_bindir}/openssl %{buildroot}%{_bindir}/libressl

#customize the conf
cat %{SOURCE1} >> %{buildroot}%{_ssldir}/libressl.cnf

# adjust developer .so links
install -m755 -d %{buildroot}%{_libdir}
rm -f %{buildroot}/%{_lib}/libcrypto.{so,la}
ln -s ../../%{_lib}/libcrypto.so.%{slibcryptov} \
  %{buildroot}%{_libdir}/libcrypto.so
mv %{buildroot}/%{_lib}/libcrypto.a %{buildroot}%{_libdir}/
rm -f %{buildroot}/%{_lib}/libssl.{so,la}
ln -s ../../%{_lib}/libssl.so.%{slibsslv} \
  %{buildroot}%{_libdir}/libssl.so
mv %{buildroot}/%{_lib}/libssl.a %{buildroot}%{_libdir}/
rm -f %{buildroot}/%{_lib}/libtls.{so,la}
ln -s ../../%{_lib}/libtls.so.%{slibtlsv} \
  %{buildroot}%{_libdir}/libtls.so
mv %{buildroot}/%{_lib}/libtls.a %{buildroot}%{_libdir}/

# adjust developer pkgconfig files
%{__sed} -i 's?libdir=.*?libdir=%{_libdir}?' \
             %{buildroot}/%{_lib}/pkgconfig/libcrypto.pc
%{__sed} -i 's?libdir=.*?libdir=%{_libdir}?' \
             %{buildroot}/%{_lib}/pkgconfig/libssl.pc
%{__sed} -i 's?libdir=.*?libdir=%{_libdir}?' \
             %{buildroot}/%{_lib}/pkgconfig/libtls.pc
%{__sed} -i 's?libdir=.*?libdir=%{_libdir}?' \
             %{buildroot}/%{_lib}/pkgconfig/openssl.pc
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/



#MODP IKE
install -p -m644 %{SOURCE20} %{buildroot}%{_pkitls}/MODP-IKE-2048-group14.pem
install -p -m644 %{SOURCE21} %{buildroot}%{_pkitls}/MODP-IKE-3072-group15.pem
install -p -m644 %{SOURCE22} %{buildroot}%{_pkitls}/MODP-IKE-4096-group16.pem
install -p -m644 %{SOURCE23} %{buildroot}%{_pkitls}/MODP-IKE-6144-group17.pem
install -p -m644 %{SOURCE24} %{buildroot}%{_pkitls}/MODP-IKE-8192-group18.pem

# initial parameters
install -p -m644 %{SOURCE20} %{buildroot}%{_pkitls}/dh2048.pem
install -p -m644 %{SOURCE21} %{buildroot}%{_pkitls}/dh3072.pem
install -p -m644 %{SOURCE22} %{buildroot}%{_pkitls}/dh4096.pem
install -p -m644 %{SOURCE25} %{buildroot}%{_pkitls}/README.DHE.md

#DH parameter generation cronjobs
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}%{_sysconfdir}/cron.monthly
cat <<EOF > %{buildroot}%{_sysconfdir}/cron.daily/generate_dh_params.sh
#!/bin/bash
TMPFILE="\`%{_bindir}/mktemp -p /tmp dhparams.XXXXXXXXXX\`"

trap "rm -f \${TMPFILE}" EXIT TERM

%{_bindir}/nice -n19 %{_bindir}/libressl dhparam -out \${TMPFILE} 2048 > /dev/null 2>&1
if [ \$? -eq 0 ]; then
  install -m644 \${TMPFILE} %{_pkitls}/dh2048.pem
fi
EOF
cat <<EOF > %{buildroot}%{_sysconfdir}/cron.monthly/generate_dh_params.sh
#!/bin/bash
TMPFILE="\`%{_bindir}/mktemp -p /tmp dhparams.XXXXXXXXXX\`"

trap "rm -f \${TMPFILE}" EXIT TERM

%{_bindir}/nice -n19 %{_bindir}/libressl dhparam -out \${TMPFILE} 3072 > /dev/null 2>&1
if [ \$? -eq 0 ]; then
  install -m644 \${TMPFILE} %{_pkitls}/dh3072.pem
fi
%{_bindir}/nice -n19 %{_bindir}/libressl dhparam -out \${TMPFILE} 4096 > /dev/null 2>&1
if [ \$? -eq 0 ]; then
  install -m644 \${TMPFILE} %{_pkitls}/dh4096.pem
fi
EOF

#fix rpath
#%%{_bindir}/chrpath -d %%{buildroot}%{_bindir}/libressl
#%%{_bindir}/chrpath -d %%{buildroot}%{_bindir}/ocspcheck
#%%{_bindir}/chrpath -d %%{buildroot}/%%{_lib}/libcrypto.so.%%{slibcryptov}
#%%{_bindir}/chrpath -d %%{buildroot}/%%{_lib}/libssl.so.%%{slibsslv}
#%%{_bindir}/chrpath -d %%{buildroot}/%%{_lib}/libtls.so.%%{slibtlsv}


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/libressl
%attr(0755,root,root) %{_bindir}/ocspcheck
%attr(0644,root,root) %{_mandir}/man1/libressl.1*
%attr(0644,root,root) %{_mandir}/man5/libressl.cnf.5*
%attr(0644,root,root) %{_mandir}/man5/x509v3.cnf.5*
%attr(0644,root,root) %{_mandir}/man8/ocspcheck.8*
%license COPYING
%doc ChangeLog COPYING README.md VERSION %{name}-make.check.log

%files libs
%defattr(-,root,root,-)
%dir %{_ssldir}/csr
%dir %{_sysconfdir}/ssl
/%{_lib}/libcrypto.so.50
%attr(0755,root,root) /%{_lib}/libcrypto.so.%{slibcryptov}
/%{_lib}/libssl.so.53
%attr(0755,root,root) /%{_lib}/libssl.so.%{slibsslv}
/%{_lib}/libtls.so.26
%attr(0755,root,root) /%{_lib}/libtls.so.%{slibtlsv}
# configuration files
%attr(0644,root,root) %config(noreplace) %{_ssldir}/libressl.cnf
%attr(0644,root,root) %config(noreplace) %{_ssldir}/x509v3.cnf
%attr(0644,root,root) %config(noreplace) %{_pkitls}/dh2048.pem
%attr(0644,root,root) %config(noreplace) %{_pkitls}/dh3072.pem
%attr(0644,root,root) %config(noreplace) %{_pkitls}/dh4096.pem
# MODP IKE
%attr(0644,root,root) %{_pkitls}/MODP-IKE-2048-group14.pem
%attr(0644,root,root) %{_pkitls}/MODP-IKE-3072-group15.pem
%attr(0644,root,root) %{_pkitls}/MODP-IKE-4096-group16.pem
%attr(0644,root,root) %{_pkitls}/MODP-IKE-6144-group17.pem
%attr(0644,root,root) %{_pkitls}/MODP-IKE-8192-group18.pem
%license COPYING
%doc ChangeLog COPYING README.md VERSION %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%{_includedir}/openssl
%{_includedir}/tls.h
%exclude %{_libdir}/libcrypto.a
%{_libdir}/libcrypto.so
%exclude %{_libdir}/libssl.a
%{_libdir}/libssl.so
%exclude %{_libdir}/libtls.a
%{_libdir}/libtls.so
%{_mandir}/man3/*.3*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files dhe-cron
%defattr(-,root,root,-)
%attr(0755,root,root) %{_sysconfdir}/cron.daily/generate_dh_params.sh
%attr(0755,root,root) %{_sysconfdir}/cron.monthly/generate_dh_params.sh
%attr(0644,root,root) %{_pkitls}/README.DHE.md
%doc README.DHE.md

%changelog
* Sun May 07 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.7.2-0.rc1
- Update to 3.7.2

* Thu Apr 27 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.6.2-0.rc3
- Fix openssldir

* Sat Mar 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.6.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
- Based on the LibreSSL packages I created for CentOS 7 (AWEL)
