Name:     libuv
Version:  1.44.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  asynchronous I/O library

Group:    System Environment/Libraries
License:  MIT
URL:      https://libuv.org/
Source0:  https://dist.libuv.org/dist/v%{version}/libuv-v%{version}.tar.gz

#BuildRequires:
#Requires:	

%description
libuv is a multi-platform support library with a focus on asynchronous
I/O. It was primarily developed for use by Node.js, but it's also used
by Luvit, Julia, uvloop, and others.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
This package includes the developer files needed to compile software
that links against the %{name} library.


%prep
%setup -n %{name}-v%{version}


%build
sh autogen.sh
%configure --disable-static
make %{?_smp_mflags}


%check
make check > %{name}-make.check.log 2>&1


%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libuv.so.1.0.0
%{_libdir}/libuv.so.1
%license LICENSE LICENSE-docs
%doc AUTHORS LICENSE ChangeLog *.md
%doc %{name}-make.check.log

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/uv.h
%dir %{_includedir}/uv
%attr(0644,root,root) %{_includedir}/uv/*.h
%{_libdir}/libuv.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libuv.pc
%license LICENSE LICENSE-docs
%doc AUTHORS LICENSE LICENSE-docs ChangeLog *.md docs



%changelog
* Wed Apr 26 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.44.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
