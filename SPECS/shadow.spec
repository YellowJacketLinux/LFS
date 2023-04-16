Name:     shadow
Version:  4.13
Release:  %{?repo}0.rc2%{?dist}
Summary:  Obfuscate user passwords hashes

Group:    System Environment/Security
License:  BSD-3-Claus
URL:      https://github.com/shadow-maint/shadow
Source0:  https://github.com/shadow-maint/shadow/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  cracklib-devel	
Requires: libsubid = %{version}-%{release}

%description
Originally, the file /etc/passwd contained both the hashed password of
users along with basic information about the user account that needs
to be publicly readable.

The shadow package increases security by moving the hashed passwords
out of that file and into a separate /etc/shadow file that is not
publicly readable, increasing the security of the hashed passwords.

%package -n libsubid
Summary:  Shared library from the shadow program
Group:    System Environment/Libraries

%description -n libsubid
The libsubid shared library from the shadow package.

%package -n libsubid-devel
Summary:  Developer files for libsubid
Group:    Development/Libraries
Requires: libsubid = %{version}-%{release}

%description -n libsubid-devel
This package contains the header files needed to compile software that
links against the shadow libsubid library.

%prep
%setup -q
[ ! -f README.md ] && cp README README.md

%build
sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /'   {} \;
find man -name Makefile.in -exec sed -i 's/getspnam\.3 / /' {} \;
find man -name Makefile.in -exec sed -i 's/passwd\.5 / /'   {} \;

# todo - min passwd length should be here
sed -e 's:#ENCRYPT_METHOD DES:ENCRYPT_METHOD SHA512:' \
    -e 's@#\(SHA_CRYPT_..._ROUNDS 5000\)@\100@'       \
    -e 's:/var/spool/mail:/var/mail:'                 \
    -e '/PATH=/{s@/sbin:@@;s@/bin:@@}'                \
    -i etc/login.defs

sed -i 's:DICTPATH.*:DICTPATH\t/lib/cracklib/pw_dict:' etc/login.defs

%configure \
  --disable-static \
  --with-libcrack \
  --with-group-name-max-length=32
make %{?_smp_mflags}


%install
make install exec_prefix=/usr DESTDIR=%{buildroot}
make -C man install-man DESTDIR=%{buildroot}
#sed -i '/MAIL/s/yes/no/' %{buildroot}%{_sysconfdir}/default/useradd

#PASS_MIN_LEN
sed -i 's/^PASS_MIN_LEN.*/PASS_MIN_LEN    8/' \
 %{buildroot}%{_sysconfdir}/login.defs

install -m755 -d %{buildroot}/bin
mv %{buildroot}%{_bindir}/login %{buildroot}/bin/
mv %{buildroot}%{_bindir}/su %{buildroot}/bin/

%find_lang %{name}

%post -n libsubid -p /sbin/ldconfig
%postun -n libsubid -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /bin/login
%attr(4755,root,root) /bin/su
%attr(4755,root,root) %{_bindir}/chage
%attr(4755,root,root) %{_bindir}/chfn
%attr(4755,root,root) %{_bindir}/chsh
%attr(4755,root,root) %{_bindir}/expiry
%attr(0755,root,root) %{_bindir}/faillog
%attr(0755,root,root) %{_bindir}/getsubids
%attr(4755,root,root) %{_bindir}/gpasswd
%attr(0755,root,root) %{_bindir}/lastlog
%attr(4755,root,root) %{_bindir}/newgidmap
%attr(4755,root,root) %{_bindir}/newgrp
%attr(4755,root,root) %{_bindir}/newuidmap
%attr(4755,root,root) %{_bindir}/passwd
%{_bindir}/sg
%{_sbindir}/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/limits
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/login.access
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/login.defs
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%license COPYING
%doc AUTHORS.md COPYING ChangeLog NEWS README.md TODO

%files -n libsubid
%defattr(-,root,root,-)
%{_libdir}/libsubid.so.4
%attr(0755,root,root) %{_libdir}/libsubid.so.4.0.0
%license COPYING
%doc COPYING

%files -n libsubid-devel
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_includedir}/shadow
%attr(0644,root,root) %{_includedir}/shadow/subid.h
%{_libdir}/libsubid.so
%attr(0644,root,root) %{_mandir}/man3/shadow.3*
%license COPYING
%doc COPYING


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.13-0.rc2
- tabs to spaces, rebuild in freshly built GCC package

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.13-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
