%if 0%{?!__meson:1} == 1
%global __meson %{_bindir}/meson
%endif
%if 0%{?!__ninja:1} == 1
%global __ninja %{_bindir}/ninja
%endif

Name:     plocate
Version:  1.1.18
Release:  %{?repo}0.dev1%{?dist}
Summary:  A much faster locate

Group:    System Environment/Utilities
License:  GPL-2.0-or-later and GPL-2.0-only
URL:      https://plocate.sesse.net/
Source0:  https://plocate.sesse.net/download/plocate-1.1.18.tar.gz

BuildRequires:  %{__meson}
BuildRequires:  %{__ninja}
BuildRequires:  pkgconfig(liburing)
#Requires:	

%description
plocate is a locate based on posting lists. Compared to mlocate,
it is much faster, and its index is much smaller. updatedb speed
is similar (or you can convert mlocate's index to plocate format
using plocate-build). It supports most mlocate options;
see --help or the man page (man -l plocate.1) for more information.


%prep
%setup -q


%build
%{__meson} setup \
  --prefix=%{_prefix} \
  obj
cd obj
%{__ninja}

# -Dinstall_cron=true \

%install
cd obj
DESTDIR=%{buildroot} %{__ninja} install
ln -s plocate %{buildroot}%{_bindir}/locate
ln -s plocate.1 %{buildroot}%{_mandir}/man1/locate.1

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/plocate
%{_bindir}/locate
%attr(0755,root,root) %{_sbindir}/plocate-build
%attr(0755,root,root) %{_sbindir}/updatedb
%attr(0644,root,root) %{_mandir}/man1/plocate.1*
%{_mandir}/man1/locate.1*
%attr(0644,root,root) %{_mandir}/man5/updatedb.conf.5*
%attr(0644,root,root) %{_mandir}/man8/plocate-build.8*
%attr(0644,root,root) %{_mandir}/man8/updatedb.8*
%dir %{_sharedstatedir}/plocate
%attr(0644,root,root) %{_sharedstatedir}/plocate/CACHEDIR.TAG
%doc



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.dev1
- Initial spec file for YJL
- Need to setup perms/cronjob (cronjob until systemd)
