# TODO - this may belong in /lib and not /usr/lib

# set to 1 to build non-CPU specific library
# %%global universalbuild 1

Name:		gmp
Version:	6.2.1
Release:	%{?repo}0.rc2%{?dist}
Summary:	Library for arbitrary precision arithmetic

Group:		System Environment/Libraries
License:	GPLv2/GPLv3 and LGPLv3
URL:		https://gmplib.org/
Source0:	https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz
Provides:       lib%{name} = %{version}-%{release}

#BuildRequires:	
#Requires:	

%description
GMP is a free library for arbitrary precision arithmetic, operating on
signed integers, rational numbers, and floating-point numbers. There
is no practical limit to the precision except the ones implied by the
available memory in the machine GMP runs on. GMP has a rich set of
functions, and the functions have a regular interface.

The main target applications for GMP are cryptography applications and
research, Internet security applications, algebra systems, computational
algebra research, etc. 

%package devel
Summary:	Development files for GMP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:       lib%{name}-devel = %{version}-%{release}

%description devel
This package contains the files necessary to compile software that
links against the GMP library.

%prep
%setup -q
%if 0%{?universalbuild} == 1
cp configfsf.guess config.guess
cp configfsf.sub config.sub
%endif


%build
%configure     \
  --enable-cxx \
  --disable-static
make %{?_smp_mflags}
make html

%install
make install DESTDIR=%{buildroot}

%check
make check > %{name}-make.check.log 2>&1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
%{_bindir}/install-info %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{_bindir}/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgmp.so.10.4.1
%attr(0755,root,root) %{_libdir}/libgmpxx.so.4.6.1
%{_libdir}/libgmp.so.10
%{_libdir}/libgmpxx.so.4
%license COPYING*
%doc %{name}-make.check.log
%doc AUTHORS COPYING* ChangeLog NEWS README

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%{_infodir}/gmp.info*
%exclude %{_infodir}/dir
%doc doc/gmp.html


%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.1-0.rc2
- Scriptlets for the gmp into file

* Wed Apr 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
