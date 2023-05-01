%if 0%{!?insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
%global novalgrind foo
%endif
%endif

Name:     libtasn1
Version:  4.19.0
Release:  %{?repo}0.rc1%{?dist}
Summary:  DER/BER data following an ASN.1 schema

Group:    System Environment/Libraries
License:  LGPL-2.1-or-later
URL:      https://www.gnu.org/software/libtasn1/
Source0:  https://ftp.gnu.org/gnu/libtasn1/libtasn1-%{version}.tar.gz

%if 0%{?runtests:1} == 1
%if 0%{!?novalgrind:1} == 1
BuildRequires:  valgrind
%endif
%endif
#Requires:

%description
Libtasn1 is the ASN.1 library used by GnuTLS, p11-kit and some other
packages. It was originally written by Fabio Fiorina, and now
maintained as a GNU package.

The goal of this implementation is to be highly portable, and only
require an ANSI C99 platform.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
License:  LGPL-2.1-or-later
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the developer files necessary to compile software
that links against the libtasn1 library.

%package utils
Group:    System Environment/Utilities
Summary:  Application utilities for libtasn
License:  GPL-3.0-or-later
Requires: %{name} = %{version}-%{release}

%description utils
This package includes the asn1Coding, asn1Decoding, and asn1Parser
utilities.

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
make -C doc/reference install-data-local

cp -p doc/COPYING ./GPL-3.0.txt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
%{insinfo} %{_infodir}/libtasn1.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libtasn1.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libtasn1.so.6.6.3
%{_libdir}/libtasn1.so.6
%license COPYING doc/COPYING.LESSER AUTHORS
%doc COPYING doc/COPYING.LESSER ChangeLog NEWS README.md THANKS
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/libtasn1.h
%{_libdir}/libtasn1.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libtasn1.pc
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/libtasn1.info*
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license COPYING doc/COPYING.LESSER AUTHORS
%doc COPYING doc/COPYING.LESSER ChangeLog NEWS README.md THANKS

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/asn1Coding
%attr(0755,root,root) %{_bindir}/asn1Decoding
%attr(0755,root,root) %{_bindir}/asn1Parser
%attr(0644,root,root) %{_mandir}/man1/asn1Coding.1*
%attr(0644,root,root) %{_mandir}/man1/asn1Decoding.1*
%attr(0644,root,root) %{_mandir}/man1/asn1Parser.1*
%license COPYING GPL-3.0.txt
%doc COPYING GPL-3.0.txt ChangeLog NEWS README.md THANKS



%changelog
* Mon May 01 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.19.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
