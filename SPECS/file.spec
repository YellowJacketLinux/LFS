Name:		file
Version:	5.44
Release:	%{?repo}0.rc2%{?dist}
Summary:	A utility for determining file types

Group:		System Environment/Libraries
License:	BSD
URL:		https://www.darwinsys.com/file/
Source0:	https://astron.com/pub/file/%{name}-%{version}.tar.gz

BuildRequires:	gcc >= 5.1.0
Requires:	libmagic = %{version}-%{release}

%description
This is Release 5.x of Ian Darwin's (copyright but distributable) file(1)
command, an implementation of the Unix File(1) command. It knows the
'magic number' of several thousands of file types. This version is the
standard "file" command for GNU/Linux, *BSD, and other systems.

%package -n libmagic
Group:		System Environment/Libraries
Summary:	The libmagic shared library

%description -n libmagic
This package contains the libmagic shared library.

%package -n libmagic-devel
Group:		Development/Libraries
Summary:	Development files for libmagic
Requires:	libmagic = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n libmagic-devel
This package contains the developer files needed to compile software
that links against the libmagic library.

%prep
%setup -q

%build
%configure \
  --libdir=/%{_lib}
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/libmagic.pc
install -m755 -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
rm -f %{buildroot}/%{_lib}/libmagic.so
ln -s ../../%{_lib}/libmagic.so.1.0.0 %{buildroot}%{_libdir}/libmagic.so

%post -n libmagic -p /sbin/ldconfig
%postun -n libmagic -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/file
%attr(0644,root,root) %{_mandir}/man1/*.1*
%license COPYING
%doc AUTHORS COPYING ChangeLog
%doc %{name}-make.check.log

%files -n libmagic
%defattr(-,root,root,-)
/%{_lib}/libmagic.so.1
%attr(0755,root,root) /%{_lib}/libmagic.so.1.0.0
%attr(0644,root,root) %{_datadir}/misc/magic.mgc
%attr(0644,root,root) %{_mandir}/man4/magic.4*
%license COPYING
%doc AUTHORS COPYING ChangeLog

%files -n libmagic-devel
%defattr(-,root,root,-)
%{_libdir}/libmagic.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libmagic.pc
%attr(0644,root,root) %{_includedir}/magic.h
%attr(0644,root,root) %{_mandir}/man3/libmagic.3*
%license COPYING


%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.44-0.rc2
- Rebuild with newly packaged gcc.

* Fri Mar 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.44-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
