%define tarname pcre2

Name:     libpcre2
Version:  10.42
Release:  %{?repo}0.rc2%{?dist}
Summary:  Perl Compatible Regular Expression libraries

Group:    System Environment/Libraries
License:  BSD-3-Clause with exception
URL:      https://www.pcre.org/
Source0:  https://github.com/PCRE2Project/pcre2/releases/download/%{tarname}-%{version}/%{tarname}-%{version}.tar.bz2

%if 0%{?runtests:1} == 1
BuildRequires:  pkgconfig(readline)
%endif
BuildRequires:  pkgconfig(zlib)
BuildRequires:  bzip2-devel

%description
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl 5. PCRE
has its own native API, as well as a set of wrapper functions that
correspond to the POSIX regular expression API. The PCRE library is
free, even for building proprietary software.

%package devel
Summary:  Development files for %{name}
Group:    System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against %{name}.

%package utils
Summary:  PCRE2 utilities
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}
Provides: %{tarname}-utils = %{version}

%description utils
This package contains the pcre2grep and pcre2test utilities.

%prep
%setup -n %{tarname}-%{version}


%build
%configure \
  --enable-unicode           \
  --enable-jit               \
  --enable-pcre2-16          \
  --enable-pcre2-32          \
  --enable-pcre2grep-libz    \
  --enable-pcre2grep-libbz2  \
  --enable-pcre2test-libreadline \
  --disable-static
make %{?_smp_mflags}

# --enable-pcre2test-libedit

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run at package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/%{tarname}
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libpcre2-8.so.0.11.2
%{_libdir}/libpcre2-8.so.0
%attr(0755,root,root) %{_libdir}/libpcre2-16.so.0.11.2
%{_libdir}/libpcre2-16.so.0
%attr(0755,root,root) %{_libdir}/libpcre2-32.so.0.11.2
%{_libdir}/libpcre2-32.so.0
%attr(0755,root,root) %{_libdir}/libpcre2-posix.so.3.0.4
%{_libdir}/libpcre2-posix.so.3
%license LICENCE
%doc doc/html AUTHORS ChangeLog HACKING LICENCE NEWS README

%files devel
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/pcre2-config
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%attr(0644,root,root) %{_mandir}/man1/pcre2-config.1*
%{_mandir}/man3/*.3*
%license LICENCE
%doc doc/html AUTHORS ChangeLog HACKING LICENCE NEWS README

%files utils
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/pcre2grep
%attr(0755,root,root) %{_bindir}/pcre2test
%attr(0644,root,root) %{_mandir}/man1/pcre2grep.1*
%attr(0644,root,root) %{_mandir}/man1/pcre2test.1*
%license LICENCE
%doc doc/html AUTHORS ChangeLog HACKING LICENCE NEWS README

%changelog
* Fri May 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 10.42-0.rc2
- Rebuild with some spec file cleanup

* Wed Mar 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 10.42-0.rc1
- Initial packaging for YJL (LFS 11.3)
