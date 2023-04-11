%define tarname xz
Name:		%{tarname}-utils
Version:	5.4.1
Release:	%{?repo}0.rc2%{?dist}
Summary:	Command line tools for XZ and LZMA compressed files

Group:		System Environment/Utilities
License:	GPLv2 plus others
URL:		https://tukaani.org/xz
Source0:	https://tukaani.org/xz/%{tarname}-%{version}.tar.xz
Provides:	%{tarname} = %{version}-%{release}
Provides:	%{tarname}-lzma = %{version}-%{release}	
Requires:	liblzma = %{version}-%{release}

%description
XZ Utils provide a general purpose data compression library
and command line tools. The native file format is the .xz
format, but also the legacy .lzma format is supported. The .xz
format supports multiple compression algorithms, of which LZMA2
is currently the primary algorithm. With typical files, XZ Utils
create about 30 % smaller files than gzip.

%package -n liblzma
Group:		System Environment/Libraries
Summary:	Library for XZ and LZMA compressed files

%description -n liblzma
liblzma is a general purpose data compression library with
an API similar to that of zlib. liblzma supports multiple
algorithms, of which LZMA2 is currently the primary algorithm.
The native file format is .xz, but also the legacy .lzma
format and raw streams (no headers at all) are supported.

This package includes the shared library.

%package -n liblzma-devel
Group:		Development/Libraries
Summary:	Library for XZ and LZMA compressed files
Requires:	liblzma = %{version}-%{release}

%description -n liblzma-devel
This package includes the API headers, static library, and
other development files related to liblzma.

%prep
%setup -n %{tarname}-%{version}


%build
%configure \
  --libdir=/%{_lib} \
  --disable-static \
  --disable-rpath
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/%{tarname}
sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/liblzma.pc
install -m755 -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
rm -f %{buildroot}/%{_lib}/liblzma.so
ln -s ../../%{_lib}/liblzma.so.5.4.1 %{buildroot}%{_libdir}/liblzma.so
%find_lang %{tarname}

%post -n liblzma -p /sbin/ldconfig
%postun -n liblzma -p /sbin/ldconfig

%files -f %{tarname}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/lzmadec
%attr(0755,root,root) %{_bindir}/lzmainfo
%attr(0755,root,root) %{_bindir}/xz
%attr(0755,root,root) %{_bindir}/xzdec
%attr(0755,root,root) %{_bindir}/xzdiff
%attr(0755,root,root) %{_bindir}/xzgrep
%attr(0755,root,root) %{_bindir}/xzless
%attr(0755,root,root) %{_bindir}/xzmore
# /usr/bin/symlinks
%{_bindir}/lzcat
%{_bindir}/lzcmp
%{_bindir}/lzdiff
%{_bindir}/lzegrep
%{_bindir}/lzfgrep
%{_bindir}/lzgrep
%{_bindir}/lzless
%{_bindir}/lzma
%{_bindir}/lzmore
%{_bindir}/unlzma
%{_bindir}/unxz
%{_bindir}/xzcat
%{_bindir}/xzcmp
%{_bindir}/xzegrep
%{_bindir}/xzfgrep
%{_mandir}/man1/*.1*
%lang(de) %{_mandir}/de/man1/*.1*
%lang(fr) %{_mandir}/fr/man1/*.1*
%lang(ko) %{_mandir}/ko/man1/*.1*
%lang(ro) %{_mandir}/ro/man1/*.1*
%lang(uk) %{_mandir}/uk/man1/*.1*
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1
%doc AUTHORS COPYING ChangeLog README THANKS TODO
%doc doc/*.txt doc/examples doc/examples_old
%doc %{name}-make.check.log

%files -n liblzma
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/liblzma.so.5.4.1
/%{_lib}/liblzma.so.5
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1

%files -n liblzma-devel
%defattr(-,root,root,-)
%{_libdir}/liblzma.so
%attr(0644,root,root) %{_libdir}/pkgconfig/liblzma.pc
%attr(0644,root,root) %{_includedir}/lzma.h
%dir %{_includedir}/lzma
%attr(0644,root,root) %{_includedir}/lzma/*.h
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1

%changelog
* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.4.1-0.rc2
- Rebuild with newly packaged gcc

* Fri Mar 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.4.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
