%global specrel 0.dev7

# Some distributions put install-info in /{,usr/}sbin
%global insinfo %{_bindir}/install-info

# buildlevel 0 is just c,c++
# buildlevel 1 adds fortran,go,objc,obj-c++
%global buildlevel 1
%if %{?repo:1}%{!?repo:0}
%if "%{?repo}" == "1.core."
%global buildlevel 0
%endif
%endif

%if %{buildlevel} == 1
%global gcc_languages c,c++,fortran,go
%global buildfortran 1
%global buildgo 1
%else
%global gcc_languages c,c++
%endif

#fixme - autoset
%global triplet x86_64-pc-linux-gnu

Name:		gcc
Version:	12.2.0
Release:	%{?repo}%{specrel}%{?dist}
Summary:	The GCC C Compiler

Group:		Development/Languages
License:	fii
URL:		https://gcc.gnu.org/
Source0:	https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz

Requires(post):	%{insinfo}
Requires(preun):	%{insinfo}
BuildRequires:	gdb
BuildRequires:	dejagnu
# not yet
%if %{buildlevel} == 1
BuildRequires:	valgrind
%endif
# not yet
#BuildRequires:	ISL
#Requires:	

%description
GCC is the GNU Compiler Collection. This package contains gcc, the C
compiler, and is needed to compile source code written in C.

%package c++
Summary:	GCC C++ compiler
Group:		Development/Languages
Requires:	libstdc++ = %{version}-%{release}
Requires:	libstdc++-devel = %{version}-%{release}

%description c++
GCC is the GNU Compiler Collection. This package contains the g++,
the C++ compiler, and is needed to compile source code written in C++.

%if 0%{?buildfortran} == 1
%package -n gfortran
Summary:	GCC fortran compiler
Group:		Development/Languages
Provides:	libgfortran-devel
Requires:	libgfortran = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n gfortran
GCC is the GNU Compiler Collection. This package contains gfortran,
the fortran compiler, and is needed to compile source code written
in fortran.
%endif

%if 0%{?buildgo} == 1
%package go
Summary:	GCC go compiler
Group:		Development/Languages
Provides:	libgo-devel
Requires:	libgo = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description go
GCC is the GNU Compiler Collection. This package contains gccgo. the
go compiler, and is needed to compile source code written in go.
%endif

%package -n cpp
Summary:	GCC C Pre-Processor
Group:		Development/Languages
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n cpp
GCC is the GNU Compiler Collection. This package contains cpp, the
C Pre-Processor.

%package -n libstdc++
Summary:	libstdc++ library
Group:		System Environment/Libraries

%description -n libstdc++
This package contains libstdc++ from the GNU Compiler Collection. This
is the standard C++ library of functions.

%package -n libstdc++-devel
Summary:	Development files for libstdc++
Group:		Development/Libraries
Requires:	libstdc++ = %{version}-%{release}

%description -n libstdc++-devel
This package contains the header files and related development files
that are needed to compile software that links against the libstdc++
library.

%package -n libstdc++-static
Summary:	libstdc++ static libraries
Group:		Development/Libraries
Requires:	libstdc++-devel = %{version}-%{release}

%description -n libstdc++-static
This package contains the libstdc++ static libraries. Most people do
not need the static libraries.

%package -n libgcc
Summary:	libcc_s library
Group:		Development/Libraries

%description -n libgcc
What a wonderful world

%if 0%{?buildfortran} == 1
%package -n libgfortran
Summary:	The libgfortran shared library
Group:		System Environment/Libraries
Requires:	libquadmath = %{version}-%{release}
Requires:	libgcc = %{version}-%{release}

%description -n libgfortran
This package contains the libgfortran shared library that is part of
the GNU Compiler Collection.

%package -n libgfortran-static
Summary:	The libgfortran static library
Group:		Development/Libraries
Requires:	gfortran = %{version}-%{release}

%description -n libgfortran-static
This package contains the static libgfortran.a library from the GNU
Compiler Collection. You probably do not need this package.
%endif

%if 0%{?buildgo} == 1
%package -n libgo
Summary:	The libgo shared library
Group:		System Environment/Libraries
Requires:       libgcc = %{version}-%{release}

%description -n libgo
This package contains the libgo shared library that is part of the GNU
Compiler Collection.

%package -n libgo-static
Summary:	The libgo static libraries
Group:		Development/Libraries
Requires:	gcc-go = %{version}-%{release}

%description -n libgo-static
This package contains the libgo static libraries that are part of the
GNU Compiler Collection. You probably do not need this package.
%endif

#
# The sanitize libraries
#

%package -n libasan
Summary:	GCC libasan shared library
Group:		System Environment/Libraries
Requires:	libgcc = %{version}-%{release}
Requires:	libstdc++ = %{version}-%{release}

%description -n libasan
This package contains the libasan shared library from the GNU Compiler
Collection.

%package -n liblsan
Summary:	liblsan shared library
Group:		System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n liblsan
The liblsan shared library

%package -n libtsan
Summary:        libtsan shared library
Group:          System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n libtsan
The libtsan shared library

%package -n libubsan
Summary:	libubsan shared library
Group:		System Environment/Libraries
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n libubsan
The libubsan shared library

%package -n libsanitizer-devel
Summary:	Developer files for the various sanitizer libraries.
Group:		Development/Libraries
Requires:	libasan  = %{version}-%{release}
Requires:	liblsan  = %{version}-%{release}
Requires:	libtsan  = %{version}-%{release}
Requires:	libubsan = %{version}-%{release}
Requires:	libstdc++-devel = %{version}-%{release}
Provides:	libasan-devel   = %{version}-%{release}
Provides:	liblsan-devel   = %{version}-%{release}
Provides:	libubsan-devel  = %{version}-%{release}

%description -n libsanitizer-devel
This package contains the developer files needed to compile software
that links against the libasan, liblsan, libtsan, and libubsan libraries.

%package -n libsanitizer-static
Summary:	GCC sanitizer static libraries
Group:		Development/Libraries
Requires:	libsanitizer-devel = %{version}-%{release}
Provides:	libasan-static
Provides:	liblsan-static
Provides:	libtsan-static
Provides:	libubsan-static

%description -n libsanitizer-static
This package contains the static libraries for libasan, liblsan, libtsan,
and libubsan.

#
# End sanitize libraries
#

%package -n libquadmath
Summary:	libquadmath shared library
Group:		System Environment/Libraries
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n libquadmath
This package includes the libquadmath shared library from the GNU
Compiler Collection.

%package -n libquadmath-static
Summary:	libquadmath static library
Group:		Development/Libraries
Requires:	gcc-libs-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains the static libquadmath.a library from the GNU
Compiler Collection. You probably do not need this package.


%package libs
Summary:	Shared libraries from GCC
Group:		System Environment/Libraries
Provides:	libatomic = %{version}-%{release}
Provides:	libcc1    = %{version}-%{release}
Provides:	libgomp   = %{version}-%{release}
Provides:	libitm    = %{version}-%{release}
Provides:	libssp    = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description libs
This package contains shared libraries that are part of the GCC collection.
It will likely be split into individual library packages in the future.

%package libs-static
Summary:	Static libraries from GCC
Group:		Development/Libraries
Provides:	libatomic-static = %{version}-%{release}
Provides:	libgomp-static   = %{version}-%{release}
Provides:	libitm-static    = %{version}-%{release}
Provides:	libssp-static    = %{version}-%{release}

%description libs-static
This package contains static libraries that are part of the GCC collection.
It will likely be split into individual library packages in the future.

%package libs-devel
Summary:	Development library symbolic links
Group:		Development/Libraries
Requires:	libquadmath = %{version}-%{release}
Requires:	gcc-libs = %{version}-%{release}

%description libs-devel
This package contains the "libfoo.so" symbolic links to libraries within
the gcc-libs package. Currently it's a packaging hack.

%package fixme
Summary:	Misc. unpackaged files
Group:		Misc

%description fixme
This package contains files that are part of GCC that still need to be
put into their proper packages.

%prep
%setup -q
# fixme - check for arch
sed -i.orig '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64


%build
mkdir build && cd build

../configure           \
  --prefix=%{_prefix}  \
  --disable-multilib   \
  --with-system-zlib   \
  --enable-linker-build-id \
  --enable-default-pie \
  --enable-default-ssp \
  --enable-languages=%{gcc_languages}

make %{?_smp_mflags}

%check
cd build
# The tests add 7+ hours on my Xeon E3 so default to no.
#  The buildsystem will have runtests set to 1.
%if 0%{?runtests} == 1
ulimit -s 32768
# there WILL be test failures, the packager should
#  examine them before distributing the package to
#  make sure they are very very few compared to
#  successes.
make -k check ||:
../contrib/test_summary > gcc-make.check.log 2>&1
%else
echo "make check not run during packaging" > gcc-make.check.log
%endif


%install
cd build
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_datadir}/gdb/auto-load/usr/lib
mv %{buildroot}/usr/lib/*gdb.py %{buildroot}%{_datadir}/gdb/auto-load/usr/lib/

[ ! -d %{buildroot}/%{_lib} ] && mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libgcc_s.so %{buildroot}/%{_lib}/
mv %{buildroot}%{_libdir}/libgcc_s.so.1 %{buildroot}/%{_lib}/
mv %{buildroot}%{_libdir}/libstdc++.so.6.0.30 %{buildroot}/%{_lib}/
rm -f %{buildroot}%{_libdir}/libstdc++.so.6
ln -sf libstdc++.so.6.0.30 %{buildroot}/%{_lib}/libstdc++.so.6
rm -f %{buildroot}%{_libdir}/libstdc++.so
ln -sf ../../%{_lib}/libstdc++.so.6.0.30 %{buildroot}%{_libdir}/libstdc++.so

[ ! -d %{buildroot}/lib ] && install -d %{buildroot}/lib
ln -sf ../usr/bin/cpp %{buildroot}/lib
ln -sf gcc %{buildroot}%{_bindir}/cc
install -d -m755 %{buildroot}/usr/lib/bfd-plugins
ln -sf ../../libexec/gcc/$(gcc -dumpmachine)/12.2.0/liblto_plugin.so \
  %{buildroot}/usr/lib/bfd-plugins/

%find_lang gcc
%find_lang cpplib
%find_lang libstdc++

#/bin/false

%post
%{insinfo} %{_infodir}/gcc.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gccinstall.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gccint.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gcc.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gccinstall.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gccint.info %{_infodir}/dir ||:
fi

%if 0%{?buildfortran} == 1
%post -n gfortran
%{insinfo} %{_infodir}/gfortran.info %{_infodir}/dir ||:

%preun -n gfortran
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gfortran.info %{_infodir}/dir ||:
fi
%endif

%if 0%{?buildgo} == 1
%post go
%{insinfo} %{_infodir}/gccgo.info %{_infodir}/dir ||:

%preun go
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gccgo.info %{_infodir}/dir ||:
fi
%endif

%post -n cpp
%{insinfo} %{_infodir}/cpp.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/cppinternals.info %{_infodir}/dir ||:

%preun -n cpp
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/cpp.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/cppinternals.info %{_infodir}/dir ||:
fi

%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig

%if 0%{?buildfortran} == 1
%post -n libgfortran -p /sbin/ldconfig
%postun -n libgfortran -p /sbin/ldconfig
%endif

%if 0%{?buildgo} == 1
%post go -p /sbin/ldconfig
%postun go -p /sbin/ldconfig
%endif

%post -n libasan -p /sbin/ldconfig
%postun -n libasan -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig
%postun -n liblsan -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig
%postun -n libtsan -p /sbin/ldconfig

%post -n libubsan -p /sbin/ldconfig
%postun -n libubsan -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
%{insinfo} %{_infodir}/libquadmath.info %{_infodir}/dir ||:

%preun -n libquadmath
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libquadmath.info %{_infodir}/dir ||:
fi

%postun -n libquadmath -p /sbin/ldconfig

%post libs
/sbin/ldconfig
%{insinfo} %{_infodir}/libgomp.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/libitm.info %{_infodir}/dir ||:

%preun libs
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libgomp.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/libitm.info %{_infodir}/dir ||:
fi

%postun libs -p /sbin/ldconfig


%files -f build/gcc.lang
%defattr(-,root,root,-)
%{_bindir}/cc
%attr(0755,root,root) %{_bindir}/gcc
%attr(0755,root,root) %{_bindir}/gcc-ar
%attr(0755,root,root) %{_bindir}/gcc-nm
%attr(0755,root,root) %{_bindir}/gcc-ranlib
%attr(0755,root,root) %{_bindir}/gcov
%attr(0755,root,root) %{_bindir}/gcov-dump
%attr(0755,root,root) %{_bindir}/gcov-tool
%attr(0755,root,root) %{_bindir}/lto-dump
%attr(0755,root,root) %{_bindir}/%{triplet}-gcc
%attr(0755,root,root) %{_bindir}/%{triplet}-gcc-%{version}
%attr(0755,root,root) %{_bindir}/%{triplet}-gcc-ar
%attr(0755,root,root) %{_bindir}/%{triplet}-gcc-nm
%attr(0755,root,root) %{_bindir}/%{triplet}-gcc-ranlib
#
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtbegin.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtbeginS.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtbeginT.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtend.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtendS.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtfastmath.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtprec32.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtprec64.o
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/crtprec80.o
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include-fixed
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include-fixed/README
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include-fixed/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include-fixed/nss
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include-fixed/nss/secport.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/fixinc_list
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/macro_list
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include/README
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include/limits.h
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcc.a
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcc_eh.a
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcov.a
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin
#%%attr(0755,root,root) %%{_prefix}/lib/gcc/%%{triplet}/%%{version}/plugin/libcc1plugin.so.0.0.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcc1plugin.so.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcc1plugin.so
#%%attr(0755,root,root) %%{_prefix}/lib/gcc/%%{triplet}/%%{version}/plugin/libcp1plugin.so.0.0.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcp1plugin.so.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcp1plugin.so
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/gtype.state
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/*.h
#
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/gcc.info*
%attr(0644,root,root) %{_infodir}/gccinstall.info*
%attr(0644,root,root) %{_infodir}/gccint.info*
%attr(0644,root,root) %{_mandir}/man1/gcc.1*
%attr(0644,root,root) %{_mandir}/man1/gcov-dump.1*
%attr(0644,root,root) %{_mandir}/man1/gcov-tool.1*
%attr(0644,root,root) %{_mandir}/man1/gcov.1*
%attr(0644,root,root) %{_mandir}/man1/lto-dump.1*
%attr(0644,root,root) %{_mandir}/man7/fsf-funding.7*
%attr(0644,root,root) %{_mandir}/man7/gfdl.7*
%attr(0644,root,root) %{_mandir}/man7/gpl.7*
%doc build/gcc-make.check.log

%files c++
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/c++
%attr(0755,root,root) %{_bindir}/g++
%attr(0755,root,root) %{_bindir}/%{triplet}-c++
%attr(0755,root,root) %{_bindir}/%{triplet}-g++
%attr(0644,root,root) %{_mandir}/man1/g++.1*

%if 0%{?buildfortran} == 1
%files -n gfortran
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gfortran
%attr(0755,root,root) %{_bindir}/%{triplet}-gfortran
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/finclude
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/finclude/*.f90
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/finclude/*.h
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/finclude/*.mod
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libcaf_single.a
%attr(0644,root,root) %{_libdir}/libgfortran.spec
%{_libdir}/libgfortran.so
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/f951
%attr(0644,root,root) %{_infodir}/gfortran.info.*
%attr(0644,root,root) %{_mandir}/man1/gfortran.1*
%endif

%if 0%{?buildgo} == 1
%files go
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gccgo
%attr(0755,root,root) %{_bindir}/go
%attr(0755,root,root) %{_bindir}/gofmt
%attr(0755,root,root) %{_bindir}/%{triplet}-gccgo
%attr(0755,root,root) %dir %{_prefix}/lib/go
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/archive
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/archive/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/compress
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/compress/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/container
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/container/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/crypto
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/crypto/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/crypto/x509
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/crypto/x509/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/database
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/database/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/database/sql
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/database/sql/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/debug
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/debug/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/encoding
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/encoding/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/go
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/go/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/go/build
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/go/build/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/hash
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/hash/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/html
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/html/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/image
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/image/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/image/color
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/image/color/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/index
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/index/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/internal
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/internal/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/io
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/io/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/log
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/log/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/math
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/math/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/mime
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/mime/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/net
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/net/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/net/http
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/net/http/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/net/rpc
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/net/rpc/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/os
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/os/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/path
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/path/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/regexp
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/regexp/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/runtime
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/runtime/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/sync
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/sync/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/testing
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/testing/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/testing/internal
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/testing/internal/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/text
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/text/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/text/template
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/text/template/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/time
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/time/*.gox
%attr(0755,root,root) %dir %{_prefix}/lib/go/%{version}/%{triplet}/unicode
%attr(0644,root,root) %{_prefix}/lib/go/%{version}/%{triplet}/unicode/*.gox
%{_libdir}/libgo.so
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/buildid
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/cgo
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/go1
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/test2json
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/vet
%attr(0644,root,root) %{_infodir}/gccgo.info*
%attr(0644,root,root) %{_mandir}/man1/gccgo.1*
%attr(0644,root,root) %{_mandir}/man1/go.1*
%attr(0644,root,root) %{_mandir}/man1/gofmt.1*
%endif

%files -n cpp -f build/cpplib.lang
%defattr(-,root,root,-)
/lib/cpp
%attr(0755,root,root) %{_bindir}/cpp
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/cc1
#
%attr(0644,root,root) %{_infodir}/cpp.info*
%attr(0644,root,root) %{_infodir}/cppinternals.info*
%attr(0644,root,root) %{_mandir}/man1/cpp.1*

%files -n libstdc++ -f build/libstdc++.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /%{_lib}/libstdc++.so.6.0.30
/%{_lib}/libstdc++.so.6
%attr(0755,root,root) %dir %{_datadir}/gcc-%{version}
%attr(0755,root,root) %dir %{_datadir}/gcc-%{version}/python
%attr(0755,root,root) %dir %{_datadir}/gcc-%{version}/python/libstdcxx
%attr(0644,root,root) %{_datadir}/gcc-%{version}/python/libstdcxx/__init__.py
%attr(0755,root,root) %dir %{_datadir}/gcc-%{version}/python/libstdcxx/v6
%attr(0644,root,root) %{_datadir}/gcc-%{version}/python/libstdcxx/v6/__init__.py
%attr(0644,root,root) %{_datadir}/gcc-%{version}/python/libstdcxx/v6/printers.py
%attr(0644,root,root) %{_datadir}/gcc-%{version}/python/libstdcxx/v6/xmethods.py
%attr(0755,root,root) %dir %{_datadir}/gdb
%attr(0755,root,root) %dir %{_datadir}/gdb/auto-load
%attr(0755,root,root) %dir %{_datadir}/gdb/auto-load/usr
%attr(0755,root,root) %dir %{_datadir}/gdb/auto-load/usr/%{_lib}
%attr(0644,root,root) %{_datadir}/gdb/auto-load/usr/%{_lib}/libstdc++.so.6.0.30-gdb.py

%files -n libstdc++-devel
%defattr(-,root,root,-)
%{_libdir}/libstdc++.so
%{_includedir}/c++
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}

%files -n libstdc++-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libstdc++.a
%attr(0644,root,root) %{_libdir}/libstdc++fs.a
%attr(0644,root,root) %{_libdir}/libsupc++.a

%files -n libgcc
%defattr(-,root,root,-)
# 0644 on these is not a typo
%attr(0644,root,root) /%{_lib}/libgcc_s.so
%attr(0644,root,root) /%{_lib}/libgcc_s.so.1

%if 0%{?buildfortran} == 1
%files -n libgfortran
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgfortran.so.5.0.0
%{_libdir}/libgfortran.so.5

%files -n libgfortran-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgfortran.a
%endif

%if 0%{?buildgo} == 1
%files -n libgo
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgo.so.21.0.0
%{_libdir}/libgo.so.21

%files -n libgo-static
%defattr(-,root,root,-)
%attr(0644,root,root)
%{_libdir}/libgo.a
%{_libdir}/libgobegin.a
%{_libdir}/libgolibbegin.a
%endif

%files -n libasan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libasan.so.8.0.0
%{_libdir}/libasan.so.8

%files -n liblsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/liblsan.so.0.0.0
%{_libdir}/liblsan.so.0

%files -n libtsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libtsan.so.2.0.0
%{_libdir}/libtsan.so.2

%files -n libubsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libubsan.so.1.0.0
%{_libdir}/libubsan.so.1

%files -n libsanitizer-devel
%defattr(-,root,root,-)
%{_libdir}/libasan.so
%{_libdir}/liblsan.so
%{_libdir}/libtsan.so
%{_libdir}/libubsan.so
# ???? check perms on next three
%{_libdir}/libasan_preinit.o
%{_libdir}/liblsan_preinit.o
%{_libdir}/libtsan_preinit.o
%attr(0644,root,root) %{_libdir}/libsanitizer.spec
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/sanitizer
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/sanitizer/*.h

%files -n libsanitizer-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libasan.a
%attr(0644,root,root) %{_libdir}/liblsan.a
%attr(0644,root,root) %{_libdir}/libtsan.a
%attr(0644,root,root) %{_libdir}/libubsan.a

%files -n libquadmath
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libquadmath.so.0.0.0
%{_libdir}/libquadmath.so.0
%attr(0644,root,root) %{_infodir}/libquadmath.info*

%files -n libquadmath-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libquadmath.a

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libatomic.so.1.2.0
%{_libdir}/libatomic.so.1
%attr(0755,root,root) %{_libdir}/libcc1.so.0.0.0
%{_libdir}/libcc1.so.0
%attr(0755,root,root) %{_libdir}/libgomp.so.1.0.0
%{_libdir}/libgomp.so.1
%attr(0755,root,root) %{_libdir}/libitm.so.1.0.0
%{_libdir}/libitm.so.1
%attr(0755,root,root) %{_libdir}/libssp.so.0.0.0
%{_libdir}/libssp.so.0
#
%attr(0644,root,root) %{_infodir}/libgomp.info*
%attr(0644,root,root) %{_infodir}/libitm.info*

%files libs-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libatomic.a
%attr(0644,root,root) %{_libdir}/libgomp.a
%attr(0644,root,root) %{_libdir}/libitm.a
%attr(0644,root,root) %{_libdir}/libssp.a
%attr(0644,root,root) %{_libdir}/libssp_nonshared.a

%files libs-devel
%{_libdir}/libatomic.so
%{_libdir}/libcc1.so
%{_libdir}/libgomp.so
%attr(0644,root,root) %{_libdir}/libgomp.spec
%{_libdir}/libitm.so
%attr(0644,root,root) %{_libdir}/libitm.spec
%{_libdir}/libquadmath.so
%{_libdir}/libssp.so

%files fixme
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin
%attr(0755,root,root) %dir %{_prefix}/lib/bfd-plugins
%{_prefix}/lib/bfd-plugins/liblto_plugin.so
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/ssp
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/ssp/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/mkheaders.conf
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%{_libexecdir}/gcc/%{triplet}/%{version}/cc1plus
%{_libexecdir}/gcc/%{triplet}/%{version}/collect2
%{_libexecdir}/gcc/%{triplet}/%{version}/g++-mapper-server
%{_libexecdir}/gcc/%{triplet}/%{version}/install-tools
%{_libexecdir}/gcc/%{triplet}/%{version}/liblto_plugin.so
%{_libexecdir}/gcc/%{triplet}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{triplet}/%{version}/lto1
%{_libexecdir}/gcc/%{triplet}/%{version}/plugin


%changelog

