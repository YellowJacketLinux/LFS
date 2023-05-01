%global sqyear 2022
%global sqlongv 3400100

%if 0%{!?__unzip:1} == 1
%global __unzip %{_bindir}/unzip
%endif

Name:     sqlite3
Version:  3.40.1
Release:  %{?repo}0.rc1%{?dist}
Summary:  self-contained SQL database engine

Group:    System Environment/Libraries
License:  Public Domain
URL:      https://sqlite.org/
Source0:  https://sqlite.org/%{sqyear}/sqlite-autoconf-%{sqlongv}.tar.gz
Source1:  https://sqlite.org/%{sqyear}/sqlite-doc-%{sqlongv}.zip

BuildRequires:  zlib-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  %__unzip

%description
SQLite is a C-language library that implements a small, fast, self-
contained, high-reliability, full-featured, SQL database engine.

%package util
Group:    System Environment/Utilities
Summary:  sqlite3 utility
Requires: %{name} = %{version}-%{release}

%description util
This package contains the sqlite3 executable utility

%package devel
Group:    Development/Libraries
Summary:  Development files for libsqlite3
Requires: %{name} = %{version}-%{release}

%description devel
The package contains the developer files needed to compile software
that links against the libsqlite3 shared library.

%prep
%setup -q -n sqlite-autoconf-%{sqlongv}
%__unzip %{SOURCE1}
START=`grep -n "Begin file sqliteInt.h" sqlite3.c |cut -d":" -f1`
END=$(($START + 11))
head -${END} sqlite3.c |tail -12 > PUBLIC_DOMAIN.txt


%build
%configure --prefix=%{_prefix} \
  --disable-static \
  --enable-fts5    \
  CPPFLAGS="-DSQLITE_ENABLE_FTS3=1            \
            -DSQLITE_ENABLE_FTS4=1            \
            -DSQLITE_ENABLE_COLUMN_METADATA=1 \
            -DSQLITE_ENABLE_UNLOCK_NOTIFY=1   \
            -DSQLITE_ENABLE_DBSTAT_VTAB=1     \
            -DSQLITE_SECURE_DELETE=1          \
            -DSQLITE_ENABLE_FTS3_TOKENIZER=1"
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libsqlite3.so.0.8.6
%{_libdir}/libsqlite3.so.0
%license PUBLIC_DOMAIN.txt
%doc PUBLIC_DOMAIN.txt

%files util
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/sqlite3
%attr(0644,root,root) %{_mandir}/man1/sqlite3.1*
%license PUBLIC_DOMAIN.txt
%doc PUBLIC_DOMAIN.txt

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/sqlite3.h
%attr(0644,root,root) %{_includedir}/sqlite3ext.h
%{_libdir}/libsqlite3.so
%attr(0644,root,root) %{_libdir}/pkgconfig/sqlite3.pc
%license PUBLIC_DOMAIN.txt
%doc PUBLIC_DOMAIN.txt
%doc sqlite-doc-%{sqlongv}



%changelog
* Mon May 1 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.40.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
