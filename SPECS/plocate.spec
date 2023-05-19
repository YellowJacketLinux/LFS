%if 0%{?!__meson:1} == 1
%global __meson %{_bindir}/meson
%endif
%if 0%{?!__ninja:1} == 1
%global __ninja %{_bindir}/ninja
%endif

Name:     plocate
Version:  1.1.18
Release:  %{?repo}0.dev4%{?dist}
Summary:  A much faster locate

Group:    System Environment/Utilities
License:  GPL-2.0-or-later and GPL-2.0-only
URL:      https://plocate.sesse.net/
Source0:  https://plocate.sesse.net/download/plocate-%{version}.tar.gz

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

# -Dsystemunitdir=%%_unitdir -Dinstall_systemd=true \

%install
cd obj
DESTDIR=%{buildroot} %{__ninja} install
ln -s plocate %{buildroot}%{_bindir}/locate
#ln -s plocate.1 %{buildroot}%{_mandir}/man1/locate.1
cat > %{buildroot}%{_mandir}/man1/locate.1 << "EOF"
.so man1/plocate.1
EOF

[ ! -d %{buildroot}%{_sysconfdir}/cron.daily ] && \
  mkdir -p %{buildroot}%{_sysconfdir}/cron.daily

cat > %{buildroot}%{_sysconfdir}/cron.daily/updatedb.sh << "EOF"
#!/bin/bash
# Update the plocate database
#
%{_bindir}/nice -n 19 %{_sbindir}/updatedb

EOF

cat > %{buildroot}%{_sysconfdir}/updatedb.conf << "EOF"
# %{_sysconfdir}/updatedb.conf
#   see man 5 updatedb.conf
#
PRUNEPATHS = "/backup"

EOF

touch %{buildroot}%{_sharedstatedir}/plocate/plocate.db

%files
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/updatedb.conf
# when systemd
#%%_unitdir/plocate-updatedb.service
#%%_unitdir/plocate-updatedb.timer
%attr(0755,root,root) %{_sysconfdir}/cron.daily/updatedb.sh
# delete above with systemd
%attr(2755,root,plocate) %{_bindir}/plocate
%{_bindir}/locate
%attr(0755,root,root) %{_sbindir}/plocate-build
%attr(0755,root,root) %{_sbindir}/updatedb
%attr(0644,root,root) %{_mandir}/man1/plocate.1*
%attr(0644,root,root) %{_mandir}/man1/locate.1*
%attr(0644,root,root) %{_mandir}/man5/updatedb.conf.5*
%attr(0644,root,root) %{_mandir}/man8/plocate-build.8*
%attr(0644,root,root) %{_mandir}/man8/updatedb.8*
%dir %{_sharedstatedir}/plocate
%attr(0644,root,root) %{_sharedstatedir}/plocate/CACHEDIR.TAG
%ghost %attr(0640,root,plocate) %verify(not md5 mtime) %{_sharedstatedir}/plocate/plocate.db
%license COPYING
%doc COPYING NEWS README



%changelog
* Fri May 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.dev4
- correct permissions (I hope), cron job until systemd is in use

* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.dev1
- Initial spec file for YJL
- Need to setup perms/cronjob (cronjob until systemd)
