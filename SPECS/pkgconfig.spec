Name:     pkgconfig
Version:  0.29.2
Release:  %{?repo}0.rc3%{?dist}
Summary:  Developer helper tool

Group:    Development/Utilities
License:  GPLv2
URL:      https://www.freedesktop.org/wiki/Software/pkg-config/
Source0:  https://pkg-config.freedesktop.org/releases/pkg-config-%{version}.tar.gz

BuildRequires:	glib-devel >= 2.0
#Requires:	

%description
pkg-config is a helper tool used when compiling applications and
libraries. It helps you insert the correct compiler options on the
command line so an application can use:
  gcc -o test test.c `pkg-config --libs --cflags glib-2.0`
for instance, rather than hard-coding values on where to find glib (or
other libraries). It is language-agnostic, so it can be used for defining
the location of documentation tools, for instance.

%prep
%setup -n pkg-config-%{version}

%build
%configure --disable-host-tool
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1 ||:

%install
make install DESTDIR=%{buildroot}
install -d %{buildroot}%{_libdir}/pkgconfig
install -d %{buildroot}%{_datadir}/pkgconfig
rm -rf %{buildroot}%{_datadir}/doc/pkg-config

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/pkg-config
%dir %attr(0755,root,root) %{_libdir}/pkgconfig
%dir %attr(0755,root,root) %{_datadir}/pkgconfig
%attr(0644,root,root) %{_datadir}/aclocal/pkg.m4
%attr(0644,root,root) %{_mandir}/man1/pkg-config.1*
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog COPYING NEWS README pkg-config-guide.html

%changelog
* Mon Apr 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.29.2-0.rc3
- Run make check

* Sun Mar 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.29.2-0.rc2
- own the pkgconfig directories

* Wed Mar 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.29.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
