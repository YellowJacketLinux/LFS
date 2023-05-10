Name:     libxml2
Version:  2.10.3
Release:  %{?repo}0.rc3%{?dist}
Summary:  XML/HTML Parser library.

Group:    System Environment/Libraries
License:  MIT
URL:      https://gitlab.gnome.org/GNOME/libxml2/-/wikis/home
Source0:  https://download.gnome.org/sources/libxml2/2.10/libxml2-%{version}.tar.xz

BuildRequires:  pkgconfig(history)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libstdc++-devel
BuildRequires:  python3-devel

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%package utils 
Summary:  The %{name} utilities
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}

%description utils
This package contains the xmlcatalog and xmllint command line utilities for
working with XML files.

%package devel
Summary:  Header files and related for %{name}.
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This packages contains the header files and related files needed to compile
software that links against %{name}.

%package -n python3-%{name}
Summary:  Python3 bindings for %{name}.
Group:    Python3
Requires: %{name} = %{version}-%{release}
%if 0%{?python3_ABI:1} == 1
# Non-Standard Macro
Requires: %{python3_ABI}
%endif

%description -n python3-%{name}
This package contains the Python3 bindings for %{name}.

%prep
%setup -q


%build
%configure \
  --disable-static \
  --with-history \
  --with-icu \
  PYTHON=%{python3} 
 
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run at package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}

mkdir rpmdoc
mv %{buildroot}%{_datadir}/doc/libxml2 rpmdoc/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libxml2.so.2.10.3
%{_libdir}/libxml2.so.2
%license Copyright
%doc README.md NEWS Copyright %{name}-make.check.log

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/xmlcatalog
%attr(0755,root,root) %{_bindir}/xmllint
%attr(0644,root,root) %{_mandir}/man1/xmlcatalog.1*
%attr(0644,root,root) %{_mandir}/man1/xmllint.1*
%license Copyright
%doc README.md NEWS Copyright

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/xml2-config
%dir %{_includedir}/libxml2
%dir %{_includedir}/libxml2/libxml
%attr(0644,root,root) %{_includedir}/libxml2/libxml/*.h
%{_libdir}/libxml2.so
%dir %{_libdir}/cmake/libxml2
%attr(0644,root,root) %{_libdir}/cmake/libxml2/libxml2-config.cmake
%attr(0644,root,root) %{_libdir}/pkgconfig/libxml-2.0.pc
%attr(0644,root,root) %{_datadir}/aclocal/libxml.m4
%attr(0644,root,root) %{_mandir}/man1/xml2-config.1*
%license Copyright
%doc README.md NEWS Copyright
%doc rpmdoc/libxml2/xmlcatalog.html
%doc rpmdoc/libxml2/xmllint.html
%doc rpmdoc/libxml2/examples
%doc rpmdoc/libxml2/tutorial
%{_datadir}/gtk-doc/html/libxml2

%files -n python3-%{name}
%defattr(-,root,root,-)
%attr(0644,root,root) %{python3_sitelib}/drv_libxml2.py
%attr(0644,root,root) %{python3_sitelib}/libxml2.py
%attr(0644,root,root) %{python3_sitelib}/__pycache__/*.pyc
%attr(0755,root,root) %{python3_sitearch}/libxml2mod.so
%doc rpmdoc/libxml2/python



%changelog
* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.10.3-0.rc3
- Major spec file cleanup.

* Tue Mar 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.10.3-0.rc2
- Cleaned up the subpackages and dependecies
- Run make check

* Sat Mar 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.10.3-0.rc1
- Initial packaging for LFS 11.3 based system
