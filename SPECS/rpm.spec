# define shared lib version
%global slibv 9.4.0

Name:		rpm
Version:	4.18.1
Release:	%{?repo}0.rc4%{?dist}
Summary:	RPM Package Manager

Group:		Utilities/Administration
License:	GPLv2 LGPLv2
URL:		https://www.rpm.org/
Source0:	https://ftp.osuosl.org/pub/rpm/releases/rpm-4.18.x/%{name}-%{version}.tar.bz2
Source1:	yjl-lfs-macros-11.3

BuildRequires:	elfutils-devel
BuildRequires:	python3-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libcap-devel
BuildRequires:	libacl-devel
BuildRequires:	libarchive-devel
BuildRequires:	libmagic-devel
BuildRequires:	libsqlite3-devel
Requires:	librpm = %{version}-%{release}

%description
The RPM package manager.

%package -n librpm
Summary:	RPM shared libraries
Group:		System Environment/Libraries

%description -n librpm
This package contains the RPM shared libraries.

%package -n librpm-manual
Summary:	HTML documentation for librpm
Group:		Development/Documentation
Requires:	librpm = %{version}-%{release}
BuildArch:	noarch

%description -n librpm-manual
This package contains HTML documentation for librpm.

%package devel
Summary:        Developer files for RPM
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       librpm = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against the RPM shared libraries.

%package -n python3-%{name}
Summary:	Python bindings for RPM
Group:		Python/Utilities
Requires:       %{name} = %{version}-%{release}
Requires:	librpm = %{version}-%{release}
%if %{?python3_ABI:1}%{!?python3_ABI:0}
# Non-Standard Macro
Requires:	%{python3_ABI}
%else
Requires:       %{python3_sitearch}
%endif

%description -n python3-%{name}
This package contains the Python3 bindings for RPM.

%prep
%setup -q


%build
%configure                 \
  --enable-zstd=yes        \
  --enable-libelf=yes      \
  --enable-ndb             \
  --enable-sqlite=yes      \
  --disable-rpath          \
  --enable-python          \
  --with-crypto=libgcrypt  \
  --disable-inhibit-plugin \
  --with-cap               \
  --with-acl
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
%find_lang rpm
install -m755 -d %{buildroot}%{_dbpath}
install -m755 -d %{buildroot}%{_sysconfdir}/rpm
install %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros
touch %{buildroot}%{_sysconfdir}/rpmrc
install -d %{buildroot}%{_sysconfdir}/cron.daily
mv %{buildroot}%{_rpmconfigdir}/rpm.daily \
  %{buildroot}%{_sysconfdir}/cron.daily/
install -d %{buildroot}%{_sysconfdir}/logrotate.d
mv %{buildroot}%{_rpmconfigdir}/rpm.log \
  %{buildroot}%{_sysconfdir}/logrotate.d/
install -m755 -d %{buildroot}%{_datadir}/doc/librpm-%{version}
cp -ar docs/librpm/html %{buildroot}%{_datadir}/doc/librpm-%{version}/

%post -n librpm -p /sbin/ldconfig
%postun -n librpm -p /sbin/ldconfig

%files -f rpm.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gendiff
%attr(0755,root,root) %{_bindir}/rpm
%attr(0755,root,root) %{_bindir}/rpm2archive
%attr(0755,root,root) %{_bindir}/rpm2cpio
%attr(0755,root,root) %{_bindir}/rpmbuild
%attr(0755,root,root) %{_bindir}/rpmdb
%attr(0755,root,root) %{_bindir}/rpmgraph
%attr(0755,root,root) %{_bindir}/rpmkeys
%attr(0755,root,root) %{_bindir}/rpmlua
%attr(0755,root,root) %{_bindir}/rpmsign
%attr(0755,root,root) %{_bindir}/rpmspec
# links in /usr/bin
%{_bindir}/rpmquery
%{_bindir}/rpmverify
##### first level _rpmconfigdir (/usr/lib/rpm) stuff
%dir %{_rpmconfigdir}
# non-exec
%attr(0644,root,root) %{_rpmconfigdir}/macros
%attr(0644,root,root) %{_rpmconfigdir}/rpmpopt-%{version}
%attr(0644,root,root) %{_rpmconfigdir}/rpmrc
## NOTE - this valgrind file may actually belong in devel?
%attr(0644,root,root) %{_rpmconfigdir}/rpm.supp
# exec stuff
%attr(0755,root,root) %{_rpmconfigdir}/brp-*
%attr(0755,root,root) %{_rpmconfigdir}/check-*
%attr(0755,root,root) %{_rpmconfigdir}/elfdeps
%attr(0755,root,root) %{_rpmconfigdir}/find-*
%attr(0755,root,root) %{_rpmconfigdir}/fontconfig.prov
%attr(0755,root,root) %{_rpmconfigdir}/mkinstalldirs
%attr(0755,root,root) %{_rpmconfigdir}/ocamldeps.sh
%attr(0755,root,root) %{_rpmconfigdir}/perl.*
%attr(0755,root,root) %{_rpmconfigdir}/pkgconfigdeps.sh
%attr(0755,root,root) %{_rpmconfigdir}/rpm2cpio.sh
%attr(0755,root,root) %{_rpmconfigdir}/rpm_macros_provides.sh
%attr(0755,root,root) %{_rpmconfigdir}/rpmdb_dump
%attr(0755,root,root) %{_rpmconfigdir}/rpmdb_load
%attr(0755,root,root) %{_rpmconfigdir}/rpmdeps
%attr(0755,root,root) %{_rpmconfigdir}/rpmuncompress
%attr(0755,root,root) %{_rpmconfigdir}/script.req
%attr(0755,root,root) %{_rpmconfigdir}/tgpg
# other /usr/lib/rpm stuff
%dir %{_prefix}/lib/rpm/fileattrs
%attr(0644,root,root) %{_prefix}/lib/rpm/fileattrs/*.attr
%dir %{_rpmluadir}
%dir %{_rpmmacrodir}
%dir %{_rpmconfigdir}/platform
%dir %{_rpmconfigdir}/platform/*
%{_rpmconfigdir}/platform/*/macros
##### plugins
%dir %{_libdir}/rpm-plugins
%attr(0755,root,root) %{_libdir}/rpm-plugins/fsverity.so
%attr(0755,root,root) %{_libdir}/rpm-plugins/ima.so
%attr(0755,root,root) %{_libdir}/rpm-plugins/prioreset.so
%attr(0755,root,root) %{_libdir}/rpm-plugins/syslog.so
##### various stuff
%dir %{_dbpath}
%dir %{_sysconfdir}/rpm
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/rpm/macros
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/rpmrc
%attr(0755,root,root) %{_sysconfdir}/cron.daily/rpm.daily
%{_sysconfdir}/logrotate.d/rpm.log
##### man pages
#%%attr(0644,root,root) %%{_mandir}/man1/*.1*
#%%lang(pl) %%attr(0644,root,root) %%{_mandir}/pl/man1/*.1*
#%%attr(0644,root,root) %%{_mandir}/man8/*.8*
#%%lang(fr) %%attr(0644,root,root) %%{_mandir}/fr/man8/*.8*
#%%lang(ja) %%attr(0644,root,root) %%{_mandir}/ja/man8/*.8*
#%%lang(ko) %%attr(0644,root,root) %%{_mandir}/ko/man8/*.8*
#%%lang(pl) %%attr(0644,root,root) %%{_mandir}/pl/man8/*.8*
#%%lang(ru) %%attr(0644,root,root) %%{_mandir}/ru/man8/*.8*
#%%lang(sk) %%attr(0644,root,root) %%{_mandir}/sk/man8/*.8*
%license COPYING
%doc COPYING CREDITS ChangeLog README docs/manual

%files -n librpm
%defattr(-,root,root,-)
##### shared libraries
%{_libdir}/librpm.so.9
%attr(0755,root,root) %{_libdir}/librpm.so.%{slibv}
%{_libdir}/librpmbuild.so.9
%attr(0755,root,root) %{_libdir}/librpmbuild.so.%{slibv}
%{_libdir}/librpmio.so.9
%attr(0755,root,root) %{_libdir}/librpmio.so.%{slibv}
%{_libdir}/librpmsign.so.9
%attr(0755,root,root) %{_libdir}/librpmsign.so.%{slibv}
%license COPYING
%doc COPYING

%files -n librpm-manual
%{_datadir}/doc/librpm-%{version}

%files devel
%defattr(-,root,root,-)
%{_includedir}/rpm
%{_libdir}/*.so
%{_libdir}/pkgconfig/rpm.pc

%files -n python3-%{name}
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{python3_sitelib}/rpm
%{python3_sitelib}/rpm/__init__.py
%{python3_sitelib}/rpm/transaction.py
%{python3_sitelib}/*.egg-info
%attr(0755,root,root) %{python3_sitearch}/rpm/_rpm.so

%changelog
* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.18.1-0.rc4
- Addition of %%insinfo to the yjl-lfs-macros-11.3 macros file.

* Tue Apr 04 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.18.1-0.rc3
- Split librpm into separate package, plus manual package
- General spec file cleanup

* Wed Mar 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.18.1-0.rc2
- Rebuild for python3_ABI requirement

* Thu Mar 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.18.1-0.rc1
- Update to 4.18.1

* Thu Mar 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.18.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
