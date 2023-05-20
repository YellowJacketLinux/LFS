%global gittag 2.3

Name:     liburing
Version:  %{gittag}
Release:	%{?repo}0.dev1%{?dist}
Summary:  Linux-native io_uring I/O access library

Group:    System Environment/Libraries
License:  (GPL-2.0-only with exceptions and LGPL-2.0-or-later) or MIT
URL:      https://git.kernel.dk/cgit/liburing/
Source0:  https://git.kernel.dk/cgit/liburing/snapshot/liburing-%{gittag}.tar.bz2

#BuildRequires:	
#Requires:	

%description
Provides native async IO for the Linux kernel, in a fast and efficient
manner, for both buffered and O_DIRECT.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package provides header files to include and libraries to link with
for the Linux-native io_uring.

%prep
%setup -q


%build
# it doesn't like %%configure
CFLAGS="${CFLAGS:--O2 -g}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:--O2 -g}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:--O2 -g }" ; export FFLAGS ;
FCFLAGS="${FCFLAGS:--O2 -g }" ; export FCFLAGS ;
LDFLAGS="${LDFLAGS:-}" ; export LDFLAGS;
./configure               \
  --prefix=%{_prefix}     \
  --libdir=%{_libdir}     \
  --libdevdir=%{_libdir}  \
  --mandir=%{_mandir}     \
  --includedir=%{_includedir}
make %{?_smp_mflags}

#%%check
#make test > %%{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/liburing.so.2.3
%{_libdir}/liburing.so.2
%license COPYING COPYING.GPL LICENSE 
%doc CHANGELOG CITATION.cff COPYING* LICENSE README SECURITY.md

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/liburing.h
%dir %{_includedir}/liburing
%attr(0644,root,root) %{_includedir}/liburing/*.h
%exclude %{_libdir}/liburing.a
%{_libdir}/liburing.so
%attr(0644,root,root) %{_libdir}/pkgconfig/liburing.pc
%attr(0644,root,root) %{_mandir}/man2/*.2*
%attr(0644,root,root) %{_mandir}/man3/*.3*
%attr(0644,root,root) %{_mandir}/man7/*.7*
%license COPYING COPYING.GPL LICENSE
%doc CHANGELOG CITATION.cff COPYING* LICENSE README SECURITY.md



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.3-0.dev1
- Initial spec file for YJL
