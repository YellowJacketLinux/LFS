%global specrel 0.rc3

### WARNING
###  Some files in the gcc package likely belong
###   elsewhere, some license tags may not be
###   correct, I have to audit that, and some
###   Requires tags may not be correct.

# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

# seems libgo should NOT be stripped
%global debug_package %{nil}
%global __strip /bin/true

# The target triplet
%if 0%{?gccbootstrap:1} == 1
%global triplet %(/opt/gcc1220/bin/gcc -dumpmachine)
%else
%global triplet %(%{_bindir}/gcc -dumpmachine)
%endif
%global karch %(uname -m)

# ISL library version 0.24
%global isldir isl-0.24

# buildlevel 0 is just c,c++,ada,d -- the languages
#  that always should be built because they are required
#  to build themselves.
# buildlevel 1 adds fortran,go,objc,obj-c++
%global buildlevel 1
%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global buildlevel 0
%endif
%endif

%if %{buildlevel} == 1
%global gcc_languages c,c++,ada,d,fortran,go,objc,obj-c++
%global buildfortran 1
%global buildgo 1
%global buildobjc 1
%else
%global gcc_languages c,c++,ada,d
%endif

Name:		gcc
Version:	12.2.0
Release:	%{?repo}%{specrel}%{?dist}
Summary:	The GCC C Compiler

Group:		Development/Languages
License:	LGPLv2, LGPLv3, GPLv2, GPLv3 w/ Runtime Exception
URL:		https://gcc.gnu.org/
Source0:	https://ftp.gnu.org/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
# isl 0.24
Source1:	https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.24.tar.bz2
BuildRequires:	binutils   >= 2.35
BuildRequires:	gawk       >= 3.1.5
BuildRequires:	make       >= 3.80
BuildRequires:	gmp-devel  >= 4.3.2
BuildRequires:	mpfr-devel >= 3.1.0
BuildRequires:	mpc-devel  >= 1.0.1
BuildRequires:	glibc-devel
BuildRequires:	zlib-devel
BuildRequires:	libzstd-devel
# below evaluates to 1 if defined
%if 0%{?gccbootstrap:1} == 1
BuildRequires:  gcc1220
# gcc1220 is a package that puts a minimal c/c++/ada/d build
#  of gcc in /opt/gcc1220
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gcc-gnat
BuildRequires:  gcc-gdc
%endif
# gdb might only be needed for tests?
BuildRequires:	gdb
%if 0%{?runtests:1} == 1
BuildRequires:  dejagnu    >= 1.5.3
BuildRequires:	expect
BuildRequires:	tcl
%if %{buildlevel} == 1
BuildRequires:	valgrind
%endif
%endif
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}


%description
GCC is the GNU Compiler Collection. This package contains gcc, the C
compiler, and is needed to compile source code written in C.

%package c++
Summary:	GCC C++ compiler
Group:		Development/Languages
License:  LGPLv2, LGPLv3, GPLv2, GPLv3 w/ Runtime Exception
Requires:	libstdc++ = %{version}-%{release}
Requires:	libstdc++-devel = %{version}-%{release}

%description c++
GCC is the GNU Compiler Collection. This package contains g++, the C++
compiler, and is needed to compile source code written in C++.

%package gnat
Summary:  GCC Ada Compiler
Group:    Development/Languages
License:  GPLv3 w/ Runtime Exception
Requires: gcc = %{version}-%{release}
Requires: adalib = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description gnat
GCC is the GNU Compiler Collection. This package contains gnat, the Ada
compiler, and is needed to compile source code written in Ada.

%package gdc
Summary:  GCC D Compiler
Group:    Development/Languages
License:  GPLv3 w/ Runtime Exception
Requires: gcc = %{version}-%{release}
Requires: libgdruntime = %{version}-%{release}
Requires: libgphobos   = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description gdc
GCC is the GNU Compiler Collection. This package containd gdc, the D
compiler, and is needed to compile source code written in D.

%if 0%{?buildfortran} == 1
%package gfortran
Summary:	GCC fortran compiler
Group:		Development/Languages
License:	GPLv3
Provides:	libgfortran-devel = %{version}-%{release}
Requires:	libgfortran = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description gfortran
GCC is the GNU Compiler Collection. This package contains gfortran,
the fortran compiler, and is needed to compile source code written
in fortran.
%endif

%if 0%{?buildgo} == 1
%package go
Summary:	GCC go compiler
Group:		Development/Languages
License:	GPLv3
Provides:	libgo-devel = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Requires:	libgo = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description go
GCC is the GNU Compiler Collection. This package contains gccgo, the
go compiler, and is needed to compile source code written in go.
%endif

%if 0%{?buildobjc} == 1
%package objc
Summary:	GCC objc/objc-c++ compile support
Group:		Development/Languages
Provides:	libobjc-devel = %{version}-%{release}
Requires:	%{name}       = %{version}-%{release}
Requires:	%{name}-c++   = %{version}-%{release}
Requires:	libobjc       = %{version}-%{release}

%description objc
GCC is the GNU Compiler Collection. This package contains the objc
and objc-c++ syntax laters, and is needed to compile software written
in objc/objc-c++
%endif

%package -n cpp
Summary:	GCC C Pre-Processor
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n cpp
GCC is the GNU Compiler Collection. This package contains cpp, the
C Pre-Processor.

%package -n libstdc++
Summary:	libstdc++ library
Group:		System Environment/Libraries
License:	GPLv3 w/ Runtime Exception
Requires:	libgcc = %{version}-%{release}

%description -n libstdc++
This package contains libstdc++ from the GNU Compiler Collection. This
is the standard C++ library of functions.

%package -n libstdc++-devel
Summary:	Development files for libstdc++
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	libstdc++   = %{version}-%{release}

%description -n libstdc++-devel
This package contains the header files and related development files
that are needed to compile software that links against the libstdc++
library.

%package -n libstdc++-static
Summary:	libstdc++ static libraries
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	libstdc++-devel = %{version}-%{release}

%description -n libstdc++-static
This package contains the libstdc++ static libraries. Most people do
not need the static libraries.

%package -n libgcc
Summary:	libcc_s library
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception

%description -n libgcc
This package contains the libgcc_s library.

%package -n adalib
Summary:  The GNU Ada libraries
Group:    System Environment/Libraries
License:  GPLv3 w/ Runtime Exception

%description -n adalib
This package contains the Ada libraries for gnat, the GNU Ada compiler.

%package -n libgdruntime
Summary:  The libgdruntime shared library
Group:    System Environment/Libraries
License:  Boost and GPLv3 w/ Runtime Exception
Requires: libgcc = %{version}-%{release}

%description -n libgdruntime
This package contains the libgdruntime shared library that is part of
the GNU compiler collection.

%package -n libgdruntime-static
Summary:  Static libgdruntime library
Group:    Development/Libraries
License:  Boost and GPLv3 w/ Runtime Exception
Requires: gcc-gdc = %{version}-%{release}

%description -n libgdruntime-static
This package contains the libgdruntime.a static library. You probably
do not need this package.

%package -n libgphobos
Summary:  The libgphobos shared library
Group:    System Environment/Libraries
License:  GPLv3
Requires: libgcc = %{version}-%{release}

%description -n libgphobos
This package contains the libgphobos shared library that is part of
the GNU compiler collection.

%package -n libgphobos-static
Summary:  The libgphobos.a static library
Group:    Development/Libraries
License:  GPLv3
Requires: gcc-gdc = %{version}-%{release}

%description -n libgphobos-static
This package contains the libgphobos.a static library. You probably
do not need this package.

%if 0%{?buildfortran} == 1
%package -n libgfortran
Summary:	The libgfortran shared library
Group:		System Environment/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	libquadmath = %{version}-%{release}
Requires:	libgcc = %{version}-%{release}

%description -n libgfortran
This package contains the libgfortran shared library that is part of
the GNU Compiler Collection.

%package -n libgfortran-static
Summary:	The libgfortran static library
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	%{name}-gfortran = %{version}-%{release}

%description -n libgfortran-static
This package contains the static libgfortran.a library from the GNU
Compiler Collection. You probably do not need this package.
%endif

%if 0%{?buildgo} == 1
%package -n libgo
Summary:	The libgo shared library
Group:		System Environment/Libraries
License:	Google MIT-Style
Requires:       libgcc = %{version}-%{release}

%description -n libgo
This package contains the libgo shared library that is part of the GNU
Compiler Collection.

%package -n libgo-static
Summary:	The libgo static libraries
Group:		Development/Libraries
License:        Google MIT-Style
Requires:	%{name}-go = %{version}-%{release}

%description -n libgo-static
This package contains the libgo static libraries that are part of the
GNU Compiler Collection. You probably do not need this package.
%endif

%if 0%{?buildobjc} == 1
%package -n libobjc
Summary:	The libobjc shared library
Group:		System Environment/Libraries
License:	GPLv3 w/ Runtime Exception
Requires:	libgcc = %{version}-%{release}

%description -n libobjc
This package contains the libobjc shared library that is part of the
GNU Compiler Collection.

%package -n libobjc-static
Summary:	The libobjc static library
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	%{name}-objc = %{version}-%{release}

%description -n libobjc-static
This package contains the libobjc.a static library that is part of the
GNU Compiler Collection. You probably do not need this package.
%endif

#
# The sanitizer libraries
#

%package -n libasan
Summary:	GCC libasan shared library
Group:		System Environment/Libraries
License:	Dual BSD-Like and MIT
Requires:	libgcc = %{version}-%{release}
Requires:	libstdc++ = %{version}-%{release}

%description -n libasan
This package contains the libasan shared library from the GNU Compiler
Collection.

%package -n liblsan
Summary:	liblsan shared library
Group:		System Environment/Libraries
License:        Dual BSD-Like and MIT
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n liblsan
The liblsan shared library

%package -n libtsan
Summary:        libtsan shared library
Group:          System Environment/Libraries
License:        Dual BSD-Like and MIT
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n libtsan
The libtsan shared library

%package -n libubsan
Summary:	libubsan shared library
Group:		System Environment/Libraries
License:        Dual BSD-Like and MIT
Requires:       libgcc = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n libubsan
The libubsan shared library

%package -n libsanitizer-devel
Summary:	Developer files for the various sanitizer libraries.
Group:		Development/Libraries
License:        Dual BSD-Like and MIT
Requires:	libasan  = %{version}-%{release}
Requires:	liblsan  = %{version}-%{release}
Requires:	libtsan  = %{version}-%{release}
Requires:	libubsan = %{version}-%{release}
Requires:	libstdc++-devel = %{version}-%{release}
Provides:	libasan-devel   = %{version}-%{release}
Provides:	liblsan-devel   = %{version}-%{release}
Provides:       libtsan-devel   = %{version}-%{release}
Provides:	libubsan-devel  = %{version}-%{release}

%description -n libsanitizer-devel
This package contains the developer files needed to compile software
that links against the libasan, liblsan, libtsan, and libubsan libraries.

%package -n libsanitizer-static
Summary:	GCC sanitizer static libraries
Group:		Development/Libraries
License:        Dual BSD-Like and MIT
Requires:	libsanitizer-devel = %{version}-%{release}
Provides:	libasan-static
Provides:	liblsan-static
Provides:	libtsan-static
Provides:	libubsan-static

%description -n libsanitizer-static
This package contains the static libraries for libasan, liblsan, libtsan,
and libubsan from the GNU Compiler Collection. You probably do not need
this package.

#
# End sanitizer libraries
#

%package -n libatomic
Summary:	libatomic shared library
Group:		System Environment/Libraries
License:	GPLv3 w/ Runtime Exception

%description -n libatomic
This package includes the libatomic shared library from the GNU
Compiler Collection.

%package -n libatomic-static
Summary:        libatomic static library
Group:          Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:       gcc-libs-devel = %{version}-%{release}

%description -n libatomic-static
This package includes the libatomic.a static library from the GNU
Compiler Collection. You probably do not need this package.

%package -n libgomp
Summary:	libgomp shared library
Group:		System Environment/Libraries
License:        GPLv3 w/ Runtime Exception
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n libgomp
This package contains the shared libgomp library from the GNU
Compiler Collection.

%package -n libgomp-static
Summary:	libgomp static library
Group:          Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:       %{name}-libs-devel = %{version}-%{release}

%description -n libgomp-static
This package contains the static libgomp.a library from the GNU
Compiler Collection. You probably do not need this package.

%package -n libitm
Summary:	libitm shared library
Group:		System Environment/Libraries
License:        GPLv3 w/ Runtime Exception
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n libitm
This package contains the libitm shared library from the GNU Compiler
Collection.

%package -n libitm-static
Summary:	libitm static library
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:       %{name}-libs-devel = %{version}-%{release}

%description -n libitm-static
This package contains the libitm.a static library from the GNU Compiler
Collection. You probably do not need this package.

%package -n libquadmath
Summary:	libquadmath shared library
Group:		System Environment/Libraries
License:	LGPLv2
Requires(post): %{insinfo}
Requires(preun):        %{insinfo}

%description -n libquadmath
This package includes the libquadmath shared library from the GNU
Compiler Collection.

%package -n libquadmath-static
Summary:	libquadmath static library
Group:		Development/Libraries
License:        LGPLv2
Requires:	%{name}-libs-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains the static libquadmath.a library from the GNU
Compiler Collection. You probably do not need this package.

%package -n libcc1
Summary:	The libcc1 shared library
Group:		System Environment/Libraries
License:	GPLv3
Requires:	libgcc    = %{version}-%{release}
Requires:       libstdc++ = %{version}-%{release}

%description -n libcc1
This package contains the libcc1 shared library from the GNU Compiler
Collection.

%package -n libcc1-devel
Summary:	Developer files for libcc1
Group:		Development/Libraries
License:        GPLv3
Requires:	libcc1          = %{version}-%{release}
Requires:	libstdc++-devel = %{version}-%{release}

%description -n libcc1-devel
This package includes the developer files needed to compile software
that links against the libcc1 library.

%package -n libssp
Summary:	The libssp shared library
Group:		System Environment/Libraries
License:        GPLv3 w/ Runtime Exception

%description -n libssp
This package contains the libssp shared library that is part of the
GNU Compiler Collection.

%package -n libssp-static
Summary:	libssp static library
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	libssp-devel = %{version}-%{release}

%description -n libssp-static
This package contains the static libssp.a library that is part of the
GNU Compiler Collection. You probably do not need this package.

%package -n libssp-devel
Summary:	libssp developer files
Group:		Development/Libraries
License:        GPLv3 w/ Runtime Exception
Requires:	libssp = %{version}-%{release}

%description -n libssp-devel
This package contains the developer files needed to build software that
links against the libssp library.

%package libs-devel
Summary:	Development library symbolic links
Group:		Development/Libraries
Requires:	libatomic   = %{version}-%{release}
Requires:	libgomp     = %{version}-%{release}
Requires:	libitm      = %{version}-%{release}
Requires:	libquadmath = %{version}-%{release}
Provides:	libatomic-devel   = %{version}-%{release}
Provides:	libgomp-devel     = %{version}-%{release}
Provides:	libitm-devel      = %{version}-%{release}
Provides:	libquadmath-devel = %{version}-%{release}

%description libs-devel
This package contains the "libfoo.so" symbolic links to libraries within
several of the GCC library packages.

%package install-tools
Summary:	GCC install-tools
Group:		Development/Utilities
Requires:	%{name} = %{version}-%{release}

%description install-tools
This package contains the install-tools that are part of the GNU
Compiler Collection.

%prep
%setup -q
tar -xf %SOURCE1
mv %{isldir} isl
# only for 64-bit using /{,usr/}lib for libraries
%if "%{karch}" == "x86_64"
%if "%{_lib}" == "lib"
sed -i.orig '/m64=/s/lib64/lib/' gcc/config/i386/t-linux64
%endif
%endif

%build
# below evaluates to 1 if defined
%if 0%{?gccbootstrap:1} == 1
export PATH="/opt/gcc1220/bin:${PATH}"
%endif

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
%if 0%{?gccbootstrap:1} == 1
export PATH="/opt/gcc1220/bin:${PATH}"
%endif
cd build
# The tests add 7+ hours on my Xeon E3 so default to no.
#  The buildsystem will have runtests set.
%if 0%{?runtests:1} == 1
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
%if 0%{?gccbootstrap:1} == 1
export PATH="/opt/gcc1220/bin:${PATH}"
%endif
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
ln -sf ../../libexec/gcc/%{triplet}/12.2.0/liblto_plugin.so \
  %{buildroot}/usr/lib/bfd-plugins/

mkdir mylibsdoc
cat > mylibsdoc/README-RPM.txt << EOF
This library package is part of the GNU Compiler Collection (GCC).
See the GCC documentation in:

    %{_datadir}/doc/gcc-%{version}

EOF

# fix doc/html reference to our packaging of the docs
sed -i 's?"doc/html"?"html"?' ../libstdc++-v3/README

%find_lang gcc
%find_lang cpplib
%find_lang libstdc++

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

%post gnat
%{insinfo} %{_infodir}/gnat-style.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gnat_rm.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gnat_ugn.info %{_infodir}/dir ||:

%preun gnat
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gnat-style.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gnat_rm.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gnat_ugn.info %{_infodir}/dir ||:
fi

%post gdc
%{insinfo} %{_infodir}/gdc.info %{_infodir}/dir ||:

%preun gdc
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gdc.info %{_infodir}/dir ||:
fi

%if 0%{?buildfortran} == 1
%post gfortran
%{insinfo} %{_infodir}/gfortran.info %{_infodir}/dir ||:

%preun gfortran
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

%post -n libgcc -p /sbin/ldconfig
%postun -n libgcc -p /sbin/ldconfig

%post -n libgdruntime -p /sbin/ldconfig
%postun -n libgdruntime -p /sbin/ldconfig

%post -n libgphobos -p /sbin/ldconfig
%postun -n libgphobos -p /sbin/ldconfig

%if 0%{?buildfortran} == 1
%post -n libgfortran -p /sbin/ldconfig
%postun -n libgfortran -p /sbin/ldconfig
%endif

%if 0%{?buildgo} == 1
%post -n libgo -p /sbin/ldconfig
%postun -n libgo -p /sbin/ldconfig
%endif

%if 0%{?buildobjc} == 1
%post -n libobjc -p /sbin/ldconfig
%postun -n libobjc -p /sbin/ldconfig
%endif

%post -n libasan -p /sbin/ldconfig
%postun -n libasan -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig
%postun -n liblsan -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig
%postun -n libtsan -p /sbin/ldconfig

%post -n libubsan -p /sbin/ldconfig
%postun -n libubsan -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig
%postun -n libatomic -p /sbin/ldconfig

%post -n libgomp
/sbin/ldconfig
%{insinfo} %{_infodir}/libgomp.info %{_infodir}/dir ||:

%preun -n libgomp
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libgomp.info %{_infodir}/dir ||:
fi

%postun -n libgomp -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
%{insinfo} %{_infodir}/libitm.info %{_infodir}/dir ||:

%preun -n libitm
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libitm.info %{_infodir}/dir ||:
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libquadmath
/sbin/ldconfig
%{insinfo} %{_infodir}/libquadmath.info %{_infodir}/dir ||:

%preun -n libquadmath
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libquadmath.info %{_infodir}/dir ||:
fi

%postun -n libquadmath -p /sbin/ldconfig

%post -n libcc1 -p /sbin/ldconfig
%postun -n libcc1 -p /sbin/ldconfig

%post -n libssp -p /sbin/ldconfig
%postun -n libssp -p /sbin/ldconfig


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
# /usr/lib stuff
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
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcc.a
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcc_eh.a
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/libgcov.a
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/gtype.state
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/*.h
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/*.def
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/b-header-vars
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/ada
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/ada/gcc-interface
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/ada/gcc-interface/ada-tree.def
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/c-family
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/c-family/c-common.def
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/c-family/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/common
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/common/config
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/common/config/i386
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/common/config/i386/i386-cpuinfo.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/config
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/config/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/config/i386
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/config/i386/*.def
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/config/i386/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/cp
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/cp/*.def
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/cp/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/d
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/d/d-tree.def
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/objc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/include/objc/objc-tree.def
# /usr/libexec stuff
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/cc1plus
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/collect2
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/liblto_plugin.so
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/lto-wrapper
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/lto1
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}/plugin
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/plugin/gengtype
# symlink into libexec
%attr(0755,root,root) %dir %{_prefix}/lib/bfd-plugins
%{_prefix}/lib/bfd-plugins/liblto_plugin.so
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
%license COPYING COPYING.LIB COPYING3 COPYING3.LIB COPYING.RUNTIME
%doc COPYING COPYING.LIB COPYING3 COPYING3.LIB COPYING.RUNTIME
%doc ChangeLog* LAST_UPDATED MAINTAINERS NEWS README
%doc build/gcc-make.check.log

%files c++
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/c++
%attr(0755,root,root) %{_bindir}/g++
%attr(0755,root,root) %{_bindir}/%{triplet}-c++
%attr(0755,root,root) %{_bindir}/%{triplet}-g++
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/g++-mapper-server
%attr(0644,root,root) %{_mandir}/man1/g++.1*
%license COPYING COPYING.LIB COPYING3 COPYING3.LIB COPYING.RUNTIME
%doc COPYING COPYING.LIB COPYING3 COPYING3.LIB COPYING.RUNTIME

%files gnat
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gnat
%attr(0755,root,root) %{_bindir}/gnatbind
%attr(0755,root,root) %{_bindir}/gnatchop
%attr(0755,root,root) %{_bindir}/gnatclean
%attr(0755,root,root) %{_bindir}/gnatkr
%attr(0755,root,root) %{_bindir}/gnatlink
%attr(0755,root,root) %{_bindir}/gnatls
%attr(0755,root,root) %{_bindir}/gnatmake
%attr(0755,root,root) %{_bindir}/gnatname
%attr(0755,root,root) %{_bindir}/gnatprep
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/ada_target_properties
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/adainclude
%attr(0444,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adainclude/*.adb
%attr(0444,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adainclude/*.ads
%attr(0444,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adainclude/*.h
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/gnat1
%attr(0644,root,root) %{_infodir}/gnat-style.info*
%attr(0644,root,root) %{_infodir}/gnat_rm.info*
%attr(0644,root,root) %{_infodir}/gnat_ugn.info*
%license COPYING3 COPYING.RUNTIME
%doc COPYING3 COPYING.RUNTIME gcc/ada/ChangeLog*

%files gdc
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gdc
%attr(0755,root,root) %{_bindir}/%{triplet}-gdc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/*.d
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/*.di
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/gc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/gc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/array
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/array/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/container
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/container/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/conservative
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/conservative/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/manual
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/manual/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/proto
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/gc/impl/proto/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/util
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/internal/util/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/stdc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/stdc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/stdcpp
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/stdcpp/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sync
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sync/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/bionic
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/bionic/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/mach
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/mach/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/netinet
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/netinet/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/darwin/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd/netinet
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd/netinet/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/dragonflybsd/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd/netinet
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd/netinet/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/freebsd/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux/netinet
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux/netinet/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/linux/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/netbsd
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/netbsd/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/netbsd/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/netbsd/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/openbsd
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/openbsd/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/openbsd/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/openbsd/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/arpa
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/arpa/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/net
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/net/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/netinet
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/netinet/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/stdc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/stdc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/posix/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/solaris
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/solaris/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/solaris/sys
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/solaris/sys/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/windows
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/windows/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/windows/stdc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/sys/windows/stdc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/thread
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/core/thread/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/etc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/etc/c
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/etc/c/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc/unwind
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc/unwind/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc/sections
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/gcc/sections/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/rt
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/rt/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/rt/util
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/rt/util/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/algorithm
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/algorithm/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/container
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/container/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/datetime
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/datetime/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/digest
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/digest/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/allocator
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/allocator/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/allocator/building_blocks
%attr(0644,root,root)
%{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/allocator/building_blocks/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/logger
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/experimental/logger/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/format
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/format/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/format/internal
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/format/internal/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/math
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/math/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/test
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/test/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/windows
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/internal/windows/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/math
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/math/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/net
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/net/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/range
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/range/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/regex
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/regex/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/regex/internal
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/regex/internal/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/uni
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/uni/*.d
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/windows
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/d/std/windows/*.d
# shared library .so symlinks
%{_libdir}/libgdruntime.so
%{_libdir}/libgphobos.so
%attr(0644,root,root) %{_libdir}/libgphobos.spec
# end shared library .so
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/d21
%attr(0644,root,root) %{_infodir}/gdc.info*
%attr(0644,root,root) %{_mandir}/man1/gdc.1*
%license COPYING3 COPYING.RUNTIME
%doc COPYING3 COPYING.RUNTIME

%if 0%{?buildfortran} == 1
%files gfortran
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
%license COPYING3
%doc COPYING3 gcc/fortran/ChangeLog*
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
%license COPYING3
%doc COPYING3 gcc/go/ChangeLog
%endif

%if 0%{?buildobjc} == 1
%files objc
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/objc
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/objc/*.h
%{_libdir}/libobjc.so
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/cc1obj
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/cc1objplus
%license COPYING3 COPYING.RUNTIME
%doc COPYING3 COPYING.RUNTIME
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
%doc build/mylibsdoc/README-RPM.txt
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README libstdc++-v3/doc/html
%doc COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libstdc++-devel
%defattr(-,root,root,-)
%{_libdir}/libstdc++.so
%{_includedir}/c++
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README libstdc++-v3/doc/html
%doc COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libstdc++-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libstdc++.a
%attr(0644,root,root) %{_libdir}/libstdc++fs.a
%attr(0644,root,root) %{_libdir}/libsupc++.a
%doc libstdc++-v3/ChangeLog* libstdc++-v3/README libstdc++-v3/doc/html
%doc COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libgcc
%defattr(-,root,root,-)
# 0644 on these is not a typo
%attr(0644,root,root) /%{_lib}/libgcc_s.so
%attr(0644,root,root) /%{_lib}/libgcc_s.so.1
%doc build/mylibsdoc/README-RPM.txt
%doc libgcc/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n adalib
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_prefix}/lib/gcc
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/adalib
%attr(0444,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/*.ali
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/*.a
%attr(0755,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/libgnarl-12.so
%attr(0755,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/libgnat-12.so
%{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/libgnarl.so
%{_prefix}/lib/gcc/%{triplet}/%{version}/adalib/libgnat.so
%license COPYING3 COPYING.RUNTIME
%doc COPYING3 COPYING.RUNTIME

%files -n libgdruntime
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgdruntime.so.3.0.0
%{_libdir}/libgdruntime.so.3
%license COPYING3 COPYING.RUNTIME libphobos/libdruntime/LICENSE.txt
%doc COPYING3 COPYING.RUNTIME libphobos/libdruntime/LICENSE.txt
%doc libphobos/README.gcc libphobos/ChangeLog
%doc build/mylibsdoc/README-RPM.txt

%files -n libgdruntime-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgdruntime.a
%license COPYING3 COPYING.RUNTIME libphobos/libdruntime/LICENSE.txt
%doc libphobos/README.gcc libphobos/ChangeLog
%doc COPYING3 COPYING.RUNTIME libphobos/libdruntime/LICENSE.txt

%files -n libgphobos
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgphobos.so.3.0.0
%{_libdir}/libgphobos.so.3
%license COPYING3
%doc COPYING3 libphobos/ChangeLog libphobos/README.gcc
%doc build/mylibsdoc/README-RPM.txt

%files -n libgphobos-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgphobos.a
%license COPYING3
%doc COPYING3 libphobos/ChangeLog libphobos/README.gcc

%if 0%{?buildfortran} == 1
%files -n libgfortran
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgfortran.so.5.0.0
%{_libdir}/libgfortran.so.5
%doc build/mylibsdoc/README-RPM.txt
%doc libgfortran/ChangeLog* COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libgfortran-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgfortran.a
%doc build/mylibsdoc/README-RPM.txt
%doc libgfortran/ChangeLog* COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME
%endif

%if 0%{?buildgo} == 1
%files -n libgo
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgo.so.21.0.0
%{_libdir}/libgo.so.21
%license libgo/LICENSE
%doc libgo/LICENSE libgo/PATENTS libgo/README libgo/VERSION
%doc build/mylibsdoc/README-RPM.txt

%files -n libgo-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgo.a
%attr(0644,root,root) %{_libdir}/libgobegin.a
%attr(0644,root,root) %{_libdir}/libgolibbegin.a
%license libgo/LICENSE
%doc libgo/LICENSE libgo/PATENTS libgo/README libgo/VERSION
%doc build/mylibsdoc/README-RPM.txt
%endif

%if 0%{?buildobjc} == 1
%files -n libobjc
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libobjc.so.4.0.0
%{_libdir}/libobjc.so.4
%license COPYING3 COPYING.RUNTIME
%doc libobjc/ChangeLog libobjc/README libobjc/THREADS
%doc build/mylibsdoc/README-RPM.txt

%files -n libobjc-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libobjc.a
%license COPYING3 COPYING.RUNTIME
%doc libobjc/ChangeLog libobjc/README libobjc/THREADS
%doc build/mylibsdoc/README-RPM.txt
%endif

%files -n libasan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libasan.so.8.0.0
%{_libdir}/libasan.so.8
%doc build/mylibsdoc/README-RPM.txt
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n liblsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/liblsan.so.0.0.0
%{_libdir}/liblsan.so.0
%doc build/mylibsdoc/README-RPM.txt
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n libtsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libtsan.so.2.0.0
%{_libdir}/libtsan.so.2
%doc build/mylibsdoc/README-RPM.txt
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n libubsan
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libubsan.so.1.0.0
%{_libdir}/libubsan.so.1
%doc build/mylibsdoc/README-RPM.txt
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n libsanitizer-devel
%defattr(-,root,root,-)
%{_libdir}/libasan.so
%{_libdir}/liblsan.so
%{_libdir}/libtsan.so
%{_libdir}/libubsan.so
%attr(0644,root,root) %{_libdir}/libasan_preinit.o
%attr(0644,root,root) %{_libdir}/liblsan_preinit.o
%attr(0644,root,root) %{_libdir}/libtsan_preinit.o
%attr(0644,root,root) %{_libdir}/libsanitizer.spec
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/sanitizer
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/sanitizer/*.h
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n libsanitizer-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libasan.a
%attr(0644,root,root) %{_libdir}/liblsan.a
%attr(0644,root,root) %{_libdir}/libtsan.a
%attr(0644,root,root) %{_libdir}/libubsan.a
%doc libsanitizer/ChangeLog libsanitizer/LICENSE.TXT
%license libsanitizer/LICENSE.TXT

%files -n libatomic
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libatomic.so.1.2.0
%{_libdir}/libatomic.so.1
%doc build/mylibsdoc/README-RPM.txt
%doc libatomic/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libatomic-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libatomic.a
%doc libatomic/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libgomp
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgomp.so.1.0.0
%{_libdir}/libgomp.so.1
%attr(0644,root,root) %{_infodir}/libgomp.info*
%doc build/mylibsdoc/README-RPM.txt
%doc libgomp/ChangeLog libgomp/ChangeLog.graphite
%doc COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libgomp-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libgomp.a
%doc libgomp/ChangeLog libgomp/ChangeLog.graphite
%doc COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libitm
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libitm.so.1.0.0
%{_libdir}/libitm.so.1
%attr(0644,root,root) %{_infodir}/libitm.info*
%doc build/mylibsdoc/README-RPM.txt
%doc libitm/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libitm-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libitm.a
%doc libitm/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libquadmath
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libquadmath.so.0.0.0
%{_libdir}/libquadmath.so.0
%attr(0644,root,root) %{_infodir}/libquadmath.info*
%doc build/mylibsdoc/README-RPM.txt
%doc libquadmath/COPYING.LIB libquadmath/ChangeLog
%license libquadmath/COPYING.LIB

%files -n libquadmath-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libquadmath.a
%doc libquadmath/COPYING.LIB libquadmath/ChangeLog
%license libquadmath/COPYING.LIB

%files -n libcc1
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libcc1.so.0.0.0
%{_libdir}/libcc1.so.0
%attr(0755,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcc1plugin.so.0.0.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcc1plugin.so.0
%attr(0755,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcp1plugin.so.0.0.0
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcp1plugin.so.0
%doc build/mylibsdoc/README-RPM.txt
%license COPYING3
%doc libcc1/ChangeLog COPYING3

%files -n libcc1-devel
%defattr(-,root,root,-)
%{_libdir}/libcc1.so
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcc1plugin.so
%{_prefix}/lib/gcc/%{triplet}/%{version}/plugin/libcp1plugin.so

%files -n libssp
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libssp.so.0.0.0
%{_libdir}/libssp.so.0
%doc build/mylibsdoc/README-RPM.txt libssp/ChangeLog
%license COPYING3 COPYING.RUNTIME

%files -n libssp-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libssp.a
%attr(0644,root,root) %{_libdir}/libssp_nonshared.a
%doc build/mylibsdoc/README-RPM.txt
%doc libssp/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files -n libssp-devel
%defattr(-,root,root,-)
%{_libdir}/libssp.so
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/include/ssp
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/include/ssp/*.h
%doc libssp/ChangeLog COPYING3 COPYING.RUNTIME
%license COPYING3 COPYING.RUNTIME

%files libs-devel
%{_libdir}/libatomic.so
%{_libdir}/libgomp.so
%attr(0644,root,root) %{_libdir}/libgomp.spec
%{_libdir}/libitm.so
%attr(0644,root,root) %{_libdir}/libitm.spec
%{_libdir}/libquadmath.so

%files install-tools
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/mkheaders.conf
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/fixinc_list
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/macro_list
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/*.h
%attr(0755,root,root) %dir %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include/README
%attr(0644,root,root) %{_prefix}/lib/gcc/%{triplet}/%{version}/install-tools/include/limits.h
#
%attr(0755,root,root) %dir %{_libexecdir}/gcc
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}
%attr(0755,root,root) %dir %{_libexecdir}/gcc/%{triplet}/%{version}/install-tools
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/install-tools/fixinc.sh
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/install-tools/fixincl
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/install-tools/mkheaders
%attr(0755,root,root) %{_libexecdir}/gcc/%{triplet}/%{version}/install-tools/mkinstalldirs

%changelog
* Fri Apr 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 12.2.0-0.rc3
- Rebuild after bootstrap build.

* Thu Apr 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 12.2.0-0.rc2
- Bootstrap build for ADA and D compilers.

* Tue Apr 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 12.2.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
