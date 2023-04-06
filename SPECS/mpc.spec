# TODO - this may belong in /lib and not /usr/lib

Name:		mpc
Version:	1.3.1
Release:	%{?repo}0.rc1%{?dist}
Summary:	Complex floating point library

Group:		System Environment/Libraries
License:	LGPLv3
URL:		https://directory.fsf.org/wiki/Mpc
Source0:	https://ftp.gnu.org/gnu/mpc/%{name}-%{version}.tar.gz

Provides:	lib%{name} = %{version}-%{release}
BuildRequires:	gmp-devel mpfr-devel
#Requires:	

%description
MPC is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result. It extends the
principles of the IEEE-754 standard for fixed precision real floating
point numbers to complex numbers, providing well-defined semantics for
every operation. At the same time, speed of operation at high precision
is a major design goal.

%package devel
Summary:	Development files for mpc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description devel
This package contains the files necessary to compile software that
links against the MPC library. 

%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}
make html

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
%{_bindir}/install-info %{_infodir}/mpc.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{_bindir}/install-info --delete %{_infodir}/mpc.info %{_infodir}/dir ||:
fi


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libmpc.so.3.3.1
%{_libdir}/libmpc.so.3
%license COPYING.LESSER
%doc AUTHORS COPYING.LESSER NEWS README TODO
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/mpc.h
%{_libdir}/libmpc.so
%attr(0644,root,root) %{_infodir}/mpc.info*
%exclude %{_infodir}/dir
%doc doc/mpc.html


%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.3.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
