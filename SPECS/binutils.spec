# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif
%global triplet %(%{_bindir}/gcc -dumpmachine)

# no stripping
%define __strip /bin/true
Name:     binutils
Version:  2.40
Release:  %{?repo}0.rc5%{?dist}
Summary:  Collection of binary tools

Group:    System Environment/Utilities
License:  GPLv2, GPLv3, LGPLv2, LGPLv3
URL:      https://www.gnu.org/software/binutils/
Source0:  https://sourceware.org/pub/binutils/releases/%{name}-%{version}.tar.xz

Requires: %{name}-libs = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}
BuildRequires:  elfutils-devel
BuildRequires:  libfl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libzstd-devel
BuildRequires:  zlib-devel

%description
These are the GNU binutils.  These are utilities of use when dealing
with binary files, either object files or executables.  These tools
consist of the linker (ld), the assembler (gas), and the profiler
(gprof) each of which have their own sub-directory named after them.
There is also a collection of other binary tools, including the
disassembler (objdump) in this directory.  These tools make use of a
pair of libraries (bfd and opcodes) and a common set of header files
(include).

%package libs
Summary:  The binutils shared libraries
Group:    System Environment/Libraries

%description libs
This package contains the binutils shared libraries.

%package devel
Summary:  Binutils developer files
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the developer files needed to compile software
that links against the binutils libraries.

%package static
Summary:  Binutils static libraries
Group:    Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains the binutils libbfd.a and libopcodes.a static
libraries. You probably do not need this package.

%package -n gprofng
Summary:  Application profiling tool
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

# from https://blogs.oracle.com/linux/post/gprofng-the-next-generation-gnu-profiling-tool
%description -n gprofng
Gprofng is a next generation application profiling tool. It supports
the profiling of programs written in C, C++, Java, or Scala running on
systems using processors from Intel, AMD, Arm, or compatible vendors.
The extent of the support is processor dependent, but the basic views
are always available.

%package -n libctf-nobfd
Summary:  The libctf-nobfd shared library
Group:    System Environment/Libraries

%description -n libctf-nobfd
This package contains the libctf-nobfd shared library from binutils.

%package -n libctf-nobfd-devel
Summary:  Developer files for the libctf-nobfd library
Group:    Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description -n libctf-nobfd-devel
This package containd the developer files needed to compile software
that links against the libctf-nobfd library.

%package -n libctf-nobfd-static
Summary:  The libctf-nobfd static library
Group:    Development/Libraries
Requires: libctf-nobfd-devel

%description -n libctf-nobfd-static
This package contains the libctf-nobfd.a static library from binutils.
You probably do not need this package.

%prep
%setup -q


%build
%configure            \
  --enable-gold       \
  --enable-ld=default \
  --enable-plugins    \
  --enable-shared     \
  --disable-werror    \
  --enable-64-bit-bfd \
  --with-system-zlib
make tooldir=/usr %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
touch files.lang
%find_lang bfd && cat bfd.lang >> files.lang
%find_lang binutils && cat binutils.lang >> files.lang
%find_lang gold && cat gold.lang >> files.lang
%find_lang gprof && cat gprof.lang >> files.lang
%find_lang ld && cat ld.lang >> files.lang
%find_lang opcodes && cat opcodes.lang >> files.lang
%find_lang gas && cat gas.lang >> files.lang

%check
%if 0%{?runtests:1} == 1
LOG=%{name}-make.check.tmp
make -k check > ${LOG} 2>&1 ||:
echo >> ${LOG}
echo >> ${LOG}
echo "##################################" >> ${LOG}
echo >> %{name}-make.check.log
echo "Failures:" >> ${LOG}
echo >> ${LOG}
echo >> ${LOG}
grep '^FAIL:' $(find -name '*.log') >> ${LOG}
sleep 1
mv ${LOG} %{name}-make.check.log
%else
echo "make check not run during packaging" > %{name}-make.check.log
%endif

%post
%{insinfo} %{_infodir}/as.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/bfd.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/binutils.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/ctf-spec.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gprof.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/ld.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/sframe-spec.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/as.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/binutils.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/ctf-spec.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gprof.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/ld.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/sframe-spec.info %{_infodir}/dir ||:
fi

%post -n gprofng
/sbin/ldconfig
%{insinfo} %{_infodir}/gprofng.info %{_infodir}/dir ||:

%preun -n gprofng
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gprofng.info %{_infodir}/dir ||:
fi

%postun -n gprofng -p /sbin/ldconfig

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post -n libctf-nobfd -p /sbin/ldconfig
%postun -n libctf-nobfd -p /sbin/ldconfig

%post devel
%{insinfo} %{_infodir}/bfd.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/bfd.info %{_infodir}/dir ||:
fi


%files -f files.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_prefix}/%{triplet}
%attr(0755,root,root) %dir %{_prefix}/%{triplet}/bin
%attr(0755,root,root) %{_prefix}/%{triplet}/bin/*
%attr(0755,root,root) %dir %{_prefix}/%{triplet}/lib
%attr(0755,root,root) %dir %{_prefix}/%{triplet}/lib/ldscripts
%attr(0644,root,root) %{_prefix}/%{triplet}/lib/ldscripts/*.x*
### bin stuff
%attr(0755,root,root) %{_bindir}/addr2line
%attr(0755,root,root) %{_bindir}/ar
%attr(0755,root,root) %{_bindir}/as
%attr(0755,root,root) %{_bindir}/c++filt
%attr(0755,root,root) %{_bindir}/dwp
%attr(0755,root,root) %{_bindir}/elfedit
%attr(0755,root,root) %{_bindir}/gprof
%attr(0755,root,root) %{_bindir}/ld
%attr(0755,root,root) %{_bindir}/ld.bfd
%attr(0755,root,root) %{_bindir}/ld.gold
%attr(0755,root,root) %{_bindir}/nm
%attr(0755,root,root) %{_bindir}/objcopy
%attr(0755,root,root) %{_bindir}/objdump
%attr(0755,root,root) %{_bindir}/ranlib
%attr(0755,root,root) %{_bindir}/readelf
%attr(0755,root,root) %{_bindir}/size
%attr(0755,root,root) %{_bindir}/strings
%attr(0755,root,root) %{_bindir}/strip
###
%dir %{_libdir}/bfd-plugins
%attr(0755,root,root) %{_libdir}/bfd-plugins/libdep.so
%exclude %{_infodir}/dir
%{_infodir}/as.info*
%{_infodir}/binutils.info*
%{_infodir}/ctf-spec.info*
%{_infodir}/gprof.info*
%{_infodir}/ld.info*
%{_infodir}/sframe-spec.info*
%attr(0644,root,root) %{_mandir}/man1/addr2line.1*
%attr(0644,root,root) %{_mandir}/man1/ar.1*
%attr(0644,root,root) %{_mandir}/man1/as.1*
%attr(0644,root,root) %{_mandir}/man1/c++filt.1*
%attr(0644,root,root) %{_mandir}/man1/dlltool.1*
%attr(0644,root,root) %{_mandir}/man1/elfedit.1*
%attr(0644,root,root) %{_mandir}/man1/gprof.1*
%attr(0644,root,root) %{_mandir}/man1/ld.1*
%attr(0644,root,root) %{_mandir}/man1/nm.1*
%attr(0644,root,root) %{_mandir}/man1/objcopy.1*
%attr(0644,root,root) %{_mandir}/man1/objdump.1*
%attr(0644,root,root) %{_mandir}/man1/ranlib.1*
%attr(0644,root,root) %{_mandir}/man1/readelf.1*
%attr(0644,root,root) %{_mandir}/man1/size.1*
%attr(0644,root,root) %{_mandir}/man1/strings.1*
%attr(0644,root,root) %{_mandir}/man1/strip.1*
%attr(0644,root,root) %{_mandir}/man1/windmc.1*
%attr(0644,root,root) %{_mandir}/man1/windres.1*
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB binutils/README
%doc %{name}-make.check.log

%files libs
%defattr(-,root,root,-)
%attr(0775,root,root) %{_libdir}/libbfd-2.40.so
%attr(0775,root,root) %{_libdir}/libopcodes-2.40.so
%attr(0775,root,root) %{_libdir}/libctf.so.0.0.0
%{_libdir}/libctf.so.0
%attr(0775,root,root) %{_libdir}/libsframe.so.0.0.0
%{_libdir}/libsframe.so.0
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so
%{_libdir}/libctf.so
%{_libdir}/libsframe.so
%{_infodir}/bfd.info*
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libbfd.a
%attr(0644,root,root) %{_libdir}/libopcodes.a
%attr(0644,root,root) %{_libdir}/libctf.a
%attr(0644,root,root) %{_libdir}/libsframe.a
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files -n gprofng
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gp-archive
%attr(0755,root,root) %{_bindir}/gp-collect-app
%attr(0755,root,root) %{_bindir}/gp-display-html
%attr(0755,root,root) %{_bindir}/gp-display-src
%attr(0755,root,root) %{_bindir}/gp-display-text
%attr(0755,root,root) %{_bindir}/gprofng
%{_sysconfdir}/gprofng.rc
%dir %{_libdir}/gprofng
%attr(0755,root,root) %{_libdir}/gprofng/libgp-collector.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-collectorAPI.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-heap.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-iotrace.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-sync.so
%attr(0755,root,root) %{_libdir}/gprofng/libgprofng.so.0.0.0
%{_libdir}/gprofng/libgprofng.so
%{_libdir}/gprofng/libgprofng.so.0
%{_infodir}/gprofng.info*
%attr(0644,root,root) %{_mandir}/man1/gp-archive.1*
%attr(0644,root,root) %{_mandir}/man1/gp-collect-app.1*
%attr(0644,root,root) %{_mandir}/man1/gp-display-html.1*
%attr(0644,root,root) %{_mandir}/man1/gp-display-src.1*
%attr(0644,root,root) %{_mandir}/man1/gp-display-text.1*
%attr(0644,root,root) %{_mandir}/man1/gprofng.1*
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files -n libctf-nobfd
%defattr(-,root,root,-)
%attr(0775,root,root) %{_libdir}/libctf-nobfd.so.0.0.0
%{_libdir}/libctf-nobfd.so.0
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files -n libctf-nobfd-devel
%defattr(-,root,root,-)
%{_libdir}/libctf-nobfd.so
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB

%files -n libctf-nobfd-static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libctf-nobfd.a
%license COPYING COPYING3 COPYING.LIB COPYING3.LIB
%doc COPYING COPYING3 COPYING.LIB COPYING3.LIB


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.40-0.rc5
- Major rewrite of spec file

* Wed Apr 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.40-0.rc4
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
- Twelve (out of numerous) test failures, all gold related
