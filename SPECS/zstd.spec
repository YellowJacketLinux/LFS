Name:		zstd
Version:	1.5.4
Release:	%{?repo}0.rc2%{?dist}
Summary:	Fast real-time compression algorithm

Group:		System Environment/Libraries
License:	GPLv2 and BSD
URL:		https://github.com/facebook/zstd
Source0:	https://github.com/facebook/zstd/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	liblzma-devel
Requires:	lib%{name} = %{version}-%{release}

%description
Zstandard, or zstd as short version, is a fast lossless compression
algorithm, targeting real-time compression scenarios at zlib-level and
better compression ratios.

Zstandard's format is stable and documented in RFC 8878.

%package -n libzstd
Summary:	The libzstd shared library
Group:		System Environment/Libraries

%description -n libzstd
This package includes the libzstd shared library.

%package -n libzstd-devel
Summary:	Developer files for lib%{name}
Group:		Development/Libraries
Requires:	lib%{name} = %{version}-%{release}

%description -n libzstd-devel
This package includes the libzstd header files and related files needed to
compile software that links against the libzstd shared library.

%prep
%setup -q


%build
make prefix=/usr

%check
make check > %{name}-make.check.log 2>&1

%install
make install prefix=%{buildroot}%{_prefix} libdir=%{buildroot}/%{_lib}
sed -i 's?libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/libzstd.pc
[ ! -d %{buildroot}%{_libdir} ] && install -m755 -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/
mv %{buildroot}/%{_lib}/libzstd.a %{buildroot}%{_libdir}/
rm -f %{buildroot}/%{_lib}/libzstd.so
ln -s ../../%{_lib}/libzstd.so.1.5.4 %{buildroot}%{_libdir}/libzstd.so

%post -n libzstd -p /sbin/ldconfig
%postun -n libzstd -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/zstd
%attr(0755,root,root) %{_bindir}/zstdgrep
%attr(0755,root,root) %{_bindir}/zstdless
%{_bindir}/unzstd
%{_bindir}/zstdcat
%{_bindir}/zstdmt
%attr(0644,root,root) %{_mandir}/man1/zstd.1*
%attr(0644,root,root) %{_mandir}/man1/zstdgrep.1*
%attr(0644,root,root) %{_mandir}/man1/zstdless.1*
%{_mandir}/man1/unzstd.1*
%{_mandir}/man1/zstdcat.1*
%license COPYING LICENSE
%doc CHANGELOG COPYING LICENSE
%doc %{name}-make.check.log

%files -n libzstd
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/libzstd.so.1.5.4
/%{_lib}/libzstd.so.1
%license COPYING LICENSE
%doc CHANGELOG COPYING LICENSE
%doc %{name}-make.check.log

%files -n libzstd-devel
%defattr(-,root,root,-)
%{_libdir}/libzstd.so
%exclude %{_libdir}/libzstd.a
%attr(0644,root,root) %{_libdir}/pkgconfig/libzstd.pc
%attr(0644,root,root) %{_includedir}/*.h
%license COPYING LICENSE
%doc doc/*.md doc/zstd_manual.html doc/educational_decoder doc/images
%doc examples

%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.5.4-0.rc2
- Rebuild with newly packaged gcc

* Fri Mar 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.5.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
