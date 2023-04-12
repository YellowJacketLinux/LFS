Name:		bzip2
Version:	1.0.8
Release:	%{?repo}0.rc2%{?dist}
Summary:	The bzip2 library

Group:		System Environment/Utilities
License:	MIT
URL:		https://sourceware.org/bzip2/
Source0:	https://www.sourceware.org/pub/%{name}/%{name}-%{version}.tar.gz

Requires:	libbz2 = %{version}-%{release}

%description
bzip2 is a freely available, patent free, high quality data compressor.

%package -n libbz2
Summary:	The %{name} shared libraries
Group:		System Environment/Libraries

%description -n libbz2
This package contains the libbz2 shared library.

%package -n libbz2-devel
Summary:	Developer files for libbz2
Group:		Development/Libraries
Requires:	libbz2 = %{version}-%{release}

%description -n libbz2-devel
This package contains the library header file for libbz2 that are
needed to compile software that links against the libbz2 library.

%prep
%setup -q


%build
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile

make -f Makefile-libbz2_so
make clean
make

%install
make PREFIX=%{buildroot}%{_prefix} install

install -m755 -d %{buildroot}/%{_lib}
cp -av libbz2.so.* %{buildroot}/%{_lib}
if [ ! -d %{buildroot}%{_libdir} ]; then
  mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
fi
ln -sv ../../%{_lib}/libbz2.so.1.0.8 %{buildroot}/%{_libdir}/libbz2.so

cp -v bzip2-shared %{buildroot}%{_bindir}/bzip2
ln -sf bzip2 %{buildroot}%{_bindir}/bzcat
ln -sf bzip2 %{buildroot}%{_bindir}/bunzip2

%post -n libbz2 -p /sbin/ldconfig
%postun -n libbz2 -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/bzdiff
%attr(0755,root,root) %{_bindir}/bzgrep
%attr(0755,root,root) %{_bindir}/bzip2
%attr(0755,root,root) %{_bindir}/bzip2recover
%attr(0755,root,root) %{_bindir}/bzmore
# /usr/bin links
%{_bindir}/bunzip2
%{_bindir}/bzcat
%{_bindir}/bzcmp
%{_bindir}/bzegrep
%{_bindir}/bzfgrep
%{_bindir}/bzless
%attr(0644,root,root) %{_mandir}/man1/*.1*
%license LICENSE
%doc CHANGES LICENSE bzip2.txt manual.html manual.ps manual.pdf

%files -n libbz2
%defattr(-,root,root,-)
/%{_lib}/libbz2.so.1.0
%license LICENSE
%attr(0755,root,root) /%{_lib}/libbz2.so.1.0.8

%files -n libbz2-devel
%defattr(-,root,root,-)
%{_libdir}/libbz2.so
%exclude %{_libdir}/libbz2.a
%attr(0644,root,root) %{_includedir}/bzlib.h
%license LICENSE



%changelog
* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.0.8-0.rc2
- Rebuild in newly packaged gcc

* Fri Mar 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.0.8-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
