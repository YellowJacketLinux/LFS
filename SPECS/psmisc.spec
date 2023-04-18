Name:     psmisc
Version:  23.6
Release:  %{?repo}0.rc1%{?dist}
Summary:  miscellaneous utilities that use the proc file-system

Group:		System Environment/Utilities
License:	GPLv2
URL:      https://gitlab.com/psmisc/psmisc
Source0:  https://sourceforge.net/projects/psmisc/files/psmisc/%{name}-%{version}.tar.xz

#BuildRequires:	
#Requires:	

%description
A package of small utilities that use the proc file-system.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/fuser
%attr(0755,root,root) %{_bindir}/killall
%attr(0755,root,root) %{_bindir}/peekfd
%attr(0755,root,root) %{_bindir}/prtstat
%attr(0755,root,root) %{_bindir}/pslog
%attr(0755,root,root) %{_bindir}/pstree
%{_bindir}/pstree.x11
%attr(0644,root,root) %{_mandir}/man1/*.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da/man1/*.1*
%lang(de) %attr(0644,root,root) %{_mandir}/de/man1/*.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/*.1*
%lang(hr) %attr(0644,root,root) %{_mandir}/hr/man1/*.1*
%lang(ko) %attr(0644,root,root) %{_mandir}/ko/man1/*.1*
%lang(pt_BR) %attr(0644,root,root) %{_mandir}/pt_BR/man1/*.1*
%lang(ro) %attr(0644,root,root) %{_mandir}/ro/man1/*.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru/man1/*.1*
%lang(sr) %attr(0644,root,root) %{_mandir}/sr/man1/*.1*
%lang(sv) %attr(0644,root,root) %{_mandir}/sv/man1/*.1*
%lang(uk) %attr(0644,root,root) %{_mandir}/uk/man1/*.1*
%license COPYING
%doc AUTHORS COPYING ChangeLog README.md



%changelog
* Mon Apr 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 23.6-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
