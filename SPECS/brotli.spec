%if 0%{?!__pip3:1} == 1
%global __pip3 %{_bindir}/pip3
%endif
%if 0%{?!__cmake:1} == 1
%global __cmake %{_bindir}/cmake
%endif

Name:     brotli
Version:  1.0.9
Release:  %{?repo}0.rc2%{?dist}
Summary:  lossless compression algorithm

Group:    System Environment/Utilities
License:  MIT
URL:      https://github.com/google/brotli
Source0:  https://github.com/google/brotli/archive/v%{version}/brotli-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  %{__pip3}
BuildRequires:  %{__cmake}
Requires:       %{name}-libs = %{version}-%{release}

%description
Brotli is a generic-purpose lossless compression algorithm that
compresses data using a combination of a modern variant of the LZ77
algorithm, Huffman coding and 2nd order context modeling, with a
compression ratio comparable to the best currently available general-
purpose compression methods. It is similar in speed with deflate but
offers more dense compression.

The specification of the Brotli Compressed Data Format is defined in
RFC 7932.

%package libs
Group:    System Environment/Libraries
Summary:  %{name} shared libraries

%description libs
This package contains the libbrotlicommon, libbrotlidec, and libbrotlienc
shared libraries.

%package devel
Group:    Development/Libraries
Summary:  %{name} development files
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains the headers files needed to compile software
that links against the libbrotlicommon, libbrotlidec, and libbrotlienc
libraries.

%package static
Group:    Development/Libraries
Summary:  %{name} static libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains the libbrotlicommon-, libbrotlidec-, and
libbrotlienc-static.a static libraries.

%package -n python3-%{name}
Group:    System Environment/Libraries
Summary:  Python3 PIP module
Requires: %{name}-libs = %{version}-%{release}
%if 0%{?python3_ABI:1} == 1
Requires: %{python3_ABI}
%endif

%description -n python3-%{name}
This package contains the Python3 bindings for %{name}

%prep
%setup -q
sed -i 's@-R..libdir.@@' scripts/*.pc.in

%build
mkdir out
cd out
%{_bindir}/cmake -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_BUILD_TYPE=Release \
      ..
make %{?_smp_mflags}
cd ..
export PIP_CONFIG_FILE=/dev/null
%{__pip3} wheel -w dist --no-build-isolation --no-deps $PWD 

%install
cd out
make install DESTDIR=%{buildroot}
cd ..
export PIP_CONFIG_FILE=/dev/null
pip3 install --no-index \
             --find-links dist \
             --no-cache-dir \
             --no-user \
             --target=%{buildroot}%{python3_sitelib} \
             Brotli

install -m755 -d %{buildroot}%{_mandir}/man1
install -m755 -d %{buildroot}%{_mandir}/man3
install -m644 docs/brotli.1 %{buildroot}%{_mandir}/man1/
install -m644 docs/constants.h.3 %{buildroot}%{_mandir}/man3/brotli-constants.h.3
install -m644 docs/decode.h.3 %{buildroot}%{_mandir}/man3/brotli-decode.h.3
install -m644 docs/encode.h.3 %{buildroot}%{_mandir}/man3/brotli-encode.h.3
install -m644 docs/types.h.3 %{buildroot}%{_mandir}/man3/brotli-types.h.3

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/brotli
%attr(0644,root,root) %{_mandir}/man1/brotli.1*
%license LICENSE
%doc LICENSE README

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libbrotlicommon.so.1.0.9
%{_libdir}/libbrotlicommon.so.1
%attr(0755,root,root) %{_libdir}/libbrotlidec.so.1.0.9
%{_libdir}/libbrotlidec.so.1
%attr(0755,root,root) %{_libdir}/libbrotlienc.so.1.0.9
%{_libdir}/libbrotlienc.so.1
%license LICENSE
%doc LICENSE README

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlidec.so
%{_libdir}/libbrotlienc.so
%attr(0644,root,root) %{_mandir}/man3/brotli-constants.h.3*
%attr(0644,root,root) %{_mandir}/man3/brotli-decode.h.3*
%attr(0644,root,root) %{_mandir}/man3/brotli-encode.h.3*
%attr(0644,root,root) %{_mandir}/man3/brotli-types.h.3*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license LICENSE
%doc LICENSE README

%files static
%defattr(-,root,root)
%attr(0644,root,root) %{_libdir}/libbrotlicommon-static.a
%attr(0644,root,root) %{_libdir}/libbrotlidec-static.a
%attr(0644,root,root) %{_libdir}/libbrotlienc-static.a
%license LICENSE
%doc LICENSE README

%files -n python3-%{name}
%defattr(-,root,root,-)
%dir %{python3_sitelib}/Brotli-%{version}.dist-info
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/INSTALLER
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/LICENSE
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/METADATA
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/RECORD
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/REQUESTED
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/WHEEL
%attr(0644,root,root) %{python3_sitelib}/Brotli-%{version}.dist-info/top_level.txt
%attr(0644,root,root) %{python3_sitelib}/__pycache__/brotli.cpython-%{python3_nodots}.pyc
%attr(0755,root,root) %{python3_sitelib}/_brotli.cpython-%{python3_nodots}-%{python3_os_platform}.so
%attr(0644,root,root) %{python3_sitelib}/brotli.py
%license LICENSE
%doc LICENSE README


%changelog
* Fri May 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.0.9-0.rc2
- Fixed build against the YJL pip.conf file

* Thu Apr 27 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.0.9-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
