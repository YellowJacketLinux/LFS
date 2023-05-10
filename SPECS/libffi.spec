%if 0%{?cpuoptimize:1} == 1
%global ffiarch native
%else
%global ffiarch x86-64
%endif

%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     libffi
Version:  3.4.4
Release:  %{?repo}0.rc1%{?dist}%{?cpuoptimize}
Summary:  A Portable Foreign Function Interface Library

Group:    System Environment/Libraries
License:  MIT
URL:      https://sourceware.org/libffi/
Source0:  https://github.com/libffi/libffi/releases/download/v%{version}/%{name}-%{version}.tar.gz

#BuildRequires:
#Requires:	

%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any
function specified by a call interface description at run-time.

FFI stands for Foreign Function Interface. A foreign function interface
is the popular name for the interface that allows code written in one
language to call code written in another language. The libffi library
really only provides the lowest, machine dependent layer of a fully
featured foreign function interface. A layer must exist above libffi
that handles type conversions for values passed between the two languages. 

%package devel
Group:    Development/Libraries
Summary:  Developer files for %{name}
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the develper files that are necessary to compile
software that links against %{name}.

%prep
%setup -q


%build
%configure --disable-static --with-gcc-arch=%{ffiarch}
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build." > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libffi.so.8.1.2
%{_libdir}/libffi.so.8
%license LICENSE
%doc LICENSE README.md %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libffi.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libffi.pc
%attr(0644,root,root) %{_infodir}/libffi.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man3/ffi.3*
%attr(0644,root,root) %{_mandir}/man3/ffi_call.3*
%attr(0644,root,root) %{_mandir}/man3/ffi_prep_cif.3*
%attr(0644,root,root) %{_mandir}/man3/ffi_prep_cif_var.3*


%changelog
* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.4.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
