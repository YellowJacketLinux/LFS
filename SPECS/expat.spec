Name:     expat
Version:  2.5.0 
Release:  %{?repo}0.1%{?dist}
Summary:  C Library for parsing XML

Group:    System Environment/Libraries
License:  MIT
URL:      https://libexpat.github.io/
Source0:  https://prdownloads.sourceforge.net/expat/expat-%{version}.tar.xz

#BuildRequires:
#Requires:

%description
Expat is a stream-oriented XML parser library written in C.

Expat excels with files too large to fit RAM, and where performance and
flexibility are crucial.

%package xmlwf
Summary:  non-validating XML checker
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}

%description xmlwf
The xmlwf is a utility to determine whether or not an XML document is
well-formed. Note that it is not a specification validator.

%package devel
Summary:  Development files for expat
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files that are needed to compile
software that links against the libexpat library.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%check
make check > %{name}-make.check.log 2>&1


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/expat

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libexpat.so.1.8.10
%{_libdir}/libexpat.so.1
%license COPYING
%doc AUTHORS Changes COPYING

%files xmlwf
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/xmlwf
%license COPYING
%doc COPYING

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%attr(0755,root,root) %dir %{_libdir}/cmake
%attr(0755,root,root) %dir %{_libdir}/cmake/expat-%{version}
%attr(0644,root,root) %{_libdir}/cmake/expat-%{version}/*.cmake
%attr(0644,root,root) %{_libdir}/pkgconfig/expat.pc
%{_libdir}/libexpat.so
%license COPYING
%doc COPYING

%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.5.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
