Name:     intltool
Version:  0.51.0
Release:  %{?repo}0.rc1%{?dist}
Summary:  internationalization utility
BuildArch:  noarch

Group:    Development/Utilities
License:  GPL-2.0-or-later
URL:      https://freedesktop.org/wiki/Software/intltool/
Source0:  https://launchpad.net/intltool/trunk/%{version}/+download/intltool-%{version}.tar.gz

#BuildRequires:
#Requires:	

%description
intltool is a set of tools to centralize translation of many different
file formats using GNU gettext-compatible PO files.


%prep
%setup -q
sed -i 's:\\\${:\\\$\\{:' intltool-update.in


%build
%configure
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/intltool-extract
%attr(0755,root,root) %{_bindir}/intltool-merge
%attr(0755,root,root) %{_bindir}/intltool-prepare
%attr(0755,root,root) %{_bindir}/intltool-update
%attr(0755,root,root) %{_bindir}/intltoolize
%attr(0644,root,root) %{_datadir}/aclocal/intltool.m4
%dir %{_datadir}/intltool
%attr(0644,root,root) %{_datadir}/intltool/Makefile.in.in
%attr(0644,root,root) %{_mandir}/man8/intltool-extract.8*
%attr(0644,root,root) %{_mandir}/man8/intltool-merge.8*
%attr(0644,root,root) %{_mandir}/man8/intltool-prepare.8*
%attr(0644,root,root) %{_mandir}/man8/intltool-update.8*
%attr(0644,root,root) %{_mandir}/man8/intltoolize.8*
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README TODO doc/I18N-HOWTO



%changelog
* Sat May 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.51.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)

