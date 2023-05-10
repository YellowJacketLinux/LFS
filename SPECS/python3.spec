%define specrel 0.rc2

%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed
%endif
%if 0%{?!__tar:1} == 1
%global __tar %{_bindir}/tar
%endif

# Version definitions
%define python3_version 3.11
%define python3_nodots 311
# General macros
%define __python3 /usr/bin/python3
%define python3 %__python3
%define python3_sitelib /usr/lib/python%{python3_version}/site-packages
%define python3_sitearch /usr/lib/python%{python3_version}/site-packages
%define python3_platform linux-%{_arch}
# YJL specific macros
%define python3_os_platform %{_arch}-linux-gnu
%define python3_API Python-%{python3_version}
%define python3_ABI %{python3_API}-%{python3_os_platform}
#

Name:     python3
Version:  %{python3_version}.3
Release:  %{?repo}%{specrel}%{?dist}
Summary:  Python3 interpreter

Group:    Programming/Languages
License:  PSF-2.0
URL:      https://www.python.org
Source0:  https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Source1:  https://www.python.org/ftp/python/doc/%{version}/python-%{version}-docs-html.tar.bz2
Source2:  rpm-macros-python-%{python3_version}
Provides: %{name}-libs = %{version}-%{release}
Provides: %{python3_API}
Provides: %{python3_ABI}

BuildRequires:  %{__sed}
BuildRequires:  %{__tar}
# This is very incomplete
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  libgdbm-devel
# Use OpenSSL, not LibreSSL --- see PEP 644
#  https://peps.python.org/pep-0644/
BuildRequires:  openssl-devel
#Requires:	

%description
Python is an interpreted, interactive, object-oriented programming
language. It incorporates modules, exceptions, dynamic typing, very
high level dynamic data types, and classes. It supports multiple
programming paradigms beyond object-oriented programming, such as
procedural and functional programming. Python combines remarkable power
with very clear syntax. It has interfaces to many system calls and
libraries, as well as to various window systems, and is extensible in
C or C++. It is also usable as an extension language for applications
that need a programmable interface. Finally, Python is portable: it
runs on many Unix variants including Linux and macOS, and on Windows.


%package devel
group:    Development/Languages
Summary:  Developer files for Python3
Requires: %{name} = %{version}

%description devel
This package includes the developer files needed to create extensions
to the python language.

%package documentation
group:    documentation
Summary:  Python 3 documentation in HTML
BuildArch:  noarch

%description documentation
This package contains the HTML documentation for Python %{version}.

%prep
%setup -n Python-%{version}


%build
%configure \
  --enable-shared \
  --with-system-expat \
  --with-system-ffi \
  --enable-optimizations
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
install -m755 -d %{buildroot}/usr/lib/rpm/macros.d
install -m644 %{SOURCE2} %{buildroot}/usr/lib/rpm/macros.d/macros.python3

# fix reference to /usr/local/bin/python
%{__sed} -i 's?/usr/local/bin/python$?%{_bindir}/python%{python3_version}?' \
  %{buildroot}/usr/lib/python%{python3_version}/cgi.py

ln -sf python%{python3_version} %{buildroot}%{_bindir}/python
install -v -m755 -d %{buildroot}%{_datadir}/doc/python-%{version}/html
%{__tar} --strip-components=1 \
    --no-same-owner           \
    --no-same-permissions     \
    -C %{buildroot}%{_datadir}/doc/python-%{version}/html \
    -xvf %{SOURCE1}

%files
%defattr(-,root,root,-)
%{_bindir}/idle3
%attr(0755,root,root) %{_bindir}/idle%{python3_version}
%{_bindir}/python
%{_bindir}/python3
%attr(0755,root,root) %{_bindir}/python%{python3_version}
%{_libdir}/libpython3.11.so
%attr(0755,root,root) %{_libdir}/libpython3.11.so.1.0
%dir /usr/lib/python%{python3_version}
%dir /usr/lib/python%{python3_version}/config-%{python3_version}-%{python3_os_platform}
/usr/lib/python%{python3_version}/LICENSE.txt
/usr/lib/python%{python3_version}/*.py
/usr/lib/python%{python3_version}/__phello__
/usr/lib/python%{python3_version}/__pycache__
/usr/lib/python%{python3_version}/asyncio
/usr/lib/python%{python3_version}/collections
/usr/lib/python%{python3_version}/concurrent
/usr/lib/python%{python3_version}/ctypes
/usr/lib/python%{python3_version}/curses
/usr/lib/python%{python3_version}/dbm
/usr/lib/python%{python3_version}/distutils
/usr/lib/python%{python3_version}/email
/usr/lib/python%{python3_version}/encodings
/usr/lib/python%{python3_version}/ensurepip
/usr/lib/python%{python3_version}/html
/usr/lib/python%{python3_version}/http
/usr/lib/python%{python3_version}/idlelib
/usr/lib/python%{python3_version}/importlib
/usr/lib/python%{python3_version}/json
/usr/lib/python%{python3_version}/lib-dynload
/usr/lib/python%{python3_version}/lib2to3
/usr/lib/python%{python3_version}/logging
/usr/lib/python%{python3_version}/multiprocessing
/usr/lib/python%{python3_version}/pydoc_data
/usr/lib/python%{python3_version}/re
/usr/lib/python%{python3_version}/site-packages
/usr/lib/python%{python3_version}/sqlite3
/usr/lib/python%{python3_version}/test
/usr/lib/python%{python3_version}/tkinter
/usr/lib/python%{python3_version}/tomllib
/usr/lib/python%{python3_version}/turtledemo
/usr/lib/python%{python3_version}/unittest
/usr/lib/python%{python3_version}/urllib
/usr/lib/python%{python3_version}/venv
/usr/lib/python%{python3_version}/wsgiref
/usr/lib/python%{python3_version}/xml
/usr/lib/python%{python3_version}/xmlrpc
/usr/lib/python%{python3_version}/zoneinfo
%{_mandir}/man1/python3*
%license LICENSE
%doc LICENSE README.rst

%files devel
%defattr(-,root,root,-)
%{_bindir}/2to3
%attr(0755,root,root) %{_bindir}/2to3-%{python3_version}
%{_bindir}/python3-config
%attr(0755,root,root) %{_bindir}/python%{python3_version}-config
%{_includedir}/python%{python3_version}
%{_libdir}/libpython3.so
%{_libdir}/pkgconfig/*.pc
/usr/lib/rpm/macros.d/macros.python3
/usr/lib/python%{python3_version}/config-%{python3_version}-%{python3_os_platform}

%files documentation
%defattr(-,root,root,-)
%{_bindir}/pydoc3
%attr(0755,root,root) %{_bindir}/pydoc%{python3_version}
%{_datadir}/doc/python-%{version}/html

%changelog
* Wed May 10 2023 Michael A. Peters <anymousepropget@gmail.com> - 3.11.3-0.rc2
- Build against OpenSSL instead of LibreSSL

* Tue Apr 25 2023 Michael A. Peters <anymousepropget@gmail.com> - 3.11.3-0.rc1
- Update to 3.11.3

* Mon Apr 03 2023 Michael A. Peters <anymousepropget@gmail.com> - 3.11.2-0.rc2
- Make /usr/bin/python symbolic link
-   NEEDS from 2023-03-22 still apply

* Wed Mar 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.11.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
-   Need to make multilib capable
-   Need to split off libs into separate package
-   Need more complete Summary/Descriptions
-   Need build deps
