%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     libtool
Version:  2.4.7
Release:  %{?repo}0.rc1%{?dist}
Summary:  Portable library support tool

Group:    Development/Utilities
License:  foo
URL:      https://www.gnu.org/software/libtool/
Source0:  https://ftp.gnu.org/gnu/libtool/libtool-%{version}.tar.xz

#BuildRequires:	
Requires: libltdl = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
GNU Libtool is a generic library support script that hides the complexity
of using shared libraries behind a consistent, portable interface.

To use Libtool, add the new generic library building commands to your
Makefile, Makefile.in, or Makefile.am. See the documentation for details. 

%package -n libltdl
Summary:  The libtool runtime library
Group:    System Environment/Libraries

%description -n libltdl
This package contains the libtool libltdl shared library.

%package -n libltdl-devel
Summary:  libltdl development files
Group:    Development/Libraries
Requires: libltdl = %{version}-%{release}

%description -n libltdl-devel
This package contains the developer files needed to compile software
that links against the libltdl library.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%check
%if 0%{?runtests:1} == 1
%if 0%{?_smp_mflags:1} == 1
export TESTSUITEFLAGS=%{?_smp_mflags}
%endif
make -k check > %{name}-make.check.log 2>&1 ||:
%else
echo "make check not run during packaging" > %{name}-make.check.log
%endif


%install
make install DESTDIR=%{buildroot}

%post
%{insinfo} %{_infodir}/libtool.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libtool.info %{_infodir}/dir ||:
fi

%post -n libltdl -p /sbin/ldconfig
%postun -n libltdl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/libtool
%attr(0755,root,root) %{_bindir}/libtoolize
%{_datadir}/aclocal
%{_datadir}/libtool
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/libtool.info*
%attr(0644,root,root) %{_mandir}/man1/libtool.1*
%attr(0644,root,root) %{_mandir}/man1/libtoolize.1*
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO

%files -n libltdl
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libltdl.so.7.3.2
%{_libdir}/libltdl.so.7
%license COPYING
%doc COPYING

%files -n libltdl-devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/ltdl.h
%attr(0755,root,root) %dir %{_includedir}/libltdl
%attr(0644,root,root) %{_includedir}/libltdl/*.h
%exclude %{_libdir}/libltdl.a
%{_libdir}/libltdl.so
%license COPYING
%doc COPYING

%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.4.7-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
