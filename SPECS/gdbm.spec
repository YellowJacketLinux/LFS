%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     gdbm
Version:  1.23
Release:  %{?repo}0.rc1%{?dist}
Summary:  GNU Database Manager

Group:		System Environment/Database
License:  GPLv3
URL:      https://www.gnu.org.ua/software/gdbm/
Source0:  https://ftp.gnu.org/gnu/gdbm/gdbm-%{version}.tar.gz

BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
Requires: libgdbm = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
GNU dbm (or GDBM, for short) is a library of database functions that
use extensible hashing and work similar to the standard UNIX dbm. These
routines are provided to a programmer needing to create and manipulate
a hashed database.

The basic use of GDBM is to store key/data pairs in a data file. Each
key must be unique and each key is paired with only one data item.

%package -n libgdbm
Summary:  The libgdbm shared library
Group:    System Environment/Libraries

%description -n libgdbm
This package contains the libgdbm library of routines for a hashed
database.

%package -n libgdbm-compat
Summary:  Compatibility library for older libgdbm API
Group:    System Environment/Libraries
Requires: libgdbm = %{version}-%{release}

%description -n libgdbm-compat
This package contains a compatibility GDBM library for software that
still needs the older than current GDBM library API.

%package -n libgdbm-devel
Summary:  libgdbm development files
Group:    Development/Libraries
Requires: libgdbm = %{version}-%{release}
Requires: libgdbm-compat = %{version}-%{release}

%description -n libgdbm-devel
This package contains the developer files needed to compile software
that links against the libgdm or libgdbm_compat libraries.

%prep
%setup -q


%build
%configure --disable-static --enable-libgdbm-compat
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang gdbm

%post
%{insinfo} %{_infodir}/gdbm.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gdbm.info %{_infodir}/dir ||:
fi

%post -n libgdbm -p /sbin/ldconfig
%postun -n libgdbm -p /sbin/ldconfig

%post -n libgdbm-compat -p /sbin/ldconfig
%postun -n libgdbm-compat -p /sbin/ldconfig

%files -f gdbm.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gdbm_dump
%attr(0755,root,root) %{_bindir}/gdbm_load
%attr(0755,root,root) %{_bindir}/gdbmtool
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/gdbm.info*
%attr(0644,root,root) %{_mandir}/man1/gdbm_dump.1*
%attr(0644,root,root) %{_mandir}/man1/gdbm_load.1*
%attr(0644,root,root) %{_mandir}/man1/gdbmtool.1*
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING NEWS NOTE-WARNING README THANKS

%files -n libgdbm
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgdbm.so.6.0.0
%{_libdir}/libgdbm.so.6
%license COPYING
%doc COPYING NOTE-WARNING

%files -n libgdbm-compat
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgdbm_compat.so.4.0.0
%{_libdir}/libgdbm_compat.so.4
%license COPYING
%doc COPYING NOTE-WARNING

%files -n libgdbm-devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm_compat.so
%attr(0644,root,root) %{_mandir}/man3/gdbm.3*
%license COPYING
%doc COPYING

%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.23-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
