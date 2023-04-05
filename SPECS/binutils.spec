# no stripping
%define __strip /bin/true
Name:		binutils
Version:	2.40
Release:	%{?repo}0.rc4%{?dist}
Summary:	Collection of binary tools

Group:		System Environment/Utilities
License:	GPLv2, GPLv3
URL:		https://www.gnu.org/software/binutils/
Source0:	https://sourceware.org/pub/binutils/releases/%{name}-%{version}.tar.xz

#BuildRequires:	
Requires:	%{name}-libs = %{version}-%{release}

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
Summary:	Binutils Libraries
Group:		System Environment/Libraries
License:	LGPLv2, LGPLv3

%description libs
This package contains the Binutils shared libraries

%package devel
Summary:	Binutils developer files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the developer files needed to compile software
that links against the binutils libraries.

%package static
Summary:	Binutils static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains the binutils static libraries, in the event
that they are actually needed.

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
LOG=%{name}=make.check.tmp
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

%post
%{_bindir}/install-info %{_infodir}/as.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/bfd.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/binutils.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/ctf-spec.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/gprof.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/gprofng.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/ld.info %{_infodir}/dir ||:
%{_bindir}/install-info %{_infodir}/sframe-spec.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{_bindir}/install-info --delete %{_infodir}/as.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/binutils.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/ctf-spec.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/gprof.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/gprofng.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/ld.info %{_infodir}/dir ||:
%{_bindir}/install-info --delete %{_infodir}/sframe-spec.info %{_infodir}/dir ||:
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post devel
%{_bindir}/install-info %{_infodir}/bfd.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{_bindir}/install-info --delete %{_infodir}/bfd.info %{_infodir}/dir ||:
fi


%files -f files.lang
%defattr(-,root,root,-)
%{_prefix}/x86_64-pc-linux-gnu
%{_sysconfdir}/gprofng.rc
%{_bindir}/*
###
%dir %{_libdir}/bfd-plugins
%attr(0755,root,root) %{_libdir}/bfd-plugins/libdep.so
%dir %{_libdir}/gprofng
%attr(0755,root,root) %{_libdir}/gprofng/libgp-collector.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-collectorAPI.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-heap.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-iotrace.so
%attr(0755,root,root) %{_libdir}/gprofng/libgp-sync.so
%attr(0755,root,root) %{_libdir}/gprofng/libgprofng.so.0.0.0
%{_libdir}/gprofng/libgprofng.so
%{_libdir}/gprofng/libgprofng.so.0
%exclude %{_infodir}/dir
%{_infodir}/as.info*
%{_infodir}/binutils.info*
%{_infodir}/ctf-spec.info*
%{_infodir}/gprof.info*
%{_infodir}/gprofng.info*
%{_infodir}/ld.info*
%{_infodir}/sframe-spec.info*
%{_mandir}/man1/*.1*
%license COPYING COPYING3
%doc COPYING COPYING3 binutils/README
%doc %{name}-make.check.log

%files libs
%defattr(-,root,root,-)
%attr(0775,root,root) %{_libdir}/libbfd-2.40.so
%attr(0775,root,root) %{_libdir}/libctf-nobfd.so.0.0.0
%attr(0775,root,root) %{_libdir}/libctf.so.0.0.0
%attr(0775,root,root) %{_libdir}/libopcodes-2.40.so
%attr(0775,root,root) %{_libdir}/libsframe.so.0.0.0
# symlinks
%{_libdir}/libctf-nobfd.so.0
%{_libdir}/libctf.so.0
%{_libdir}/libsframe.so.0
%license COPYING.LIB COPYING3.LIB
%doc COPYING.LIB COPYING3.LIB 

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libbfd.so
%{_infodir}/bfd.info*
%{_libdir}/libctf-nobfd.so
%{_libdir}/libctf.so
%{_libdir}/libopcodes.so
%{_libdir}/libsframe.so

%files static
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libbfd.a
%attr(0644,root,root) %{_libdir}/libctf-nobfd.a
%attr(0644,root,root) %{_libdir}/libctf.a
%attr(0644,root,root) %{_libdir}/libopcodes.a
%attr(0644,root,root) %{_libdir}/libsframe.a

%changelog
* Wed Apr 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.40-0.rc4
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
- Twelve (out of numerous) test failures, all gold related
