%if 0%{?!__meson:1} == 1
%global __meson %{_bindir}/meson
%endif
%if 0%{?!__ninja:1} == 1
%global __ninja %{_bindir}/ninja
%endif

Name:     plocate
Version:  1.1.18
Release:  %{?repo}0.rc4%{?dist}
Summary:  A much faster locate

Group:    System Environment/Utilities
License:  GPL-2.0-or-later and GPL-2.0-only
URL:      https://plocate.sesse.net/
Source0:  https://plocate.sesse.net/download/plocate-%{version}.tar.gz
Patch0:   plocate-1.1.18-remove-plocate-build.patch

BuildRequires:  %{__meson}
BuildRequires:  %{__ninja}
BuildRequires:  pkgconfig(liburing)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  libstdc++-devel
%if 0%{?_yjl_sysusers:1} == 1
Requires(pre): %{_yjl_sysusers}
%endif


%description
plocate is a locate based on posting lists. Compared to mlocate,
it is much faster, and its index is much smaller. updatedb speed
is similar (or you can convert mlocate's index to plocate format
using plocate-build). It supports most mlocate options;
see --help or the man page (man -l plocate.1) for more information.


%prep
%setup -q
%patch 0 -p1


%build
%{__meson} setup          \
  --prefix=%{_prefix}     \
  -Dinstall_systemd=false \
  obj
cd obj
%{__ninja}

# If systemD files are wanted...
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
  mkdir -p %{buildroot}%{_sysconfdir}/cron.hourly

cat > %{buildroot}%{_sysconfdir}/cron.hourly/updatedb.sh << "EOF"
#!/bin/bash
# Update the plocate database
#   9900 = two hours, 45 minutes

CURT=`%{_bindir}/date +%s`
MODT=`%{_bindir}/stat -c '%Y' %{_sharedstatedir}/plocate/plocate.db` ||\
  MODT=0
DIFF=$(($CURT-$MODT))
if [ $DIFF -gt 9900 ]; then
  %{_bindir}/nice -n 19 %{_sbindir}/updatedb
fi

EOF

cat > %{buildroot}%{_sysconfdir}/updatedb.conf << "EOF"
# %{_sysconfdir}/updatedb.conf
#   see man 5 updatedb.conf
#
PRUNEPATHS = "/backup /opt/texlive"

EOF

touch %{buildroot}%{_sharedstatedir}/plocate/plocate.db

%pre
%if 0%{?_yjl_sysusers:1} == 1
%{_yjl_sysusers} --useradd False plocate
%else
getent group plocate >/dev/null 2>&1 ||groupadd -r plocate
%endif

%files
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/updatedb.conf
%attr(0755,root,root) %{_sysconfdir}/cron.hourly/updatedb.sh
%attr(2755,root,plocate) %{_bindir}/plocate
%{_bindir}/locate
%attr(0755,root,root) %{_sbindir}/updatedb
%attr(0644,root,root) %{_mandir}/man1/plocate.1*
%attr(0644,root,root) %{_mandir}/man1/locate.1*
%attr(0644,root,root) %{_mandir}/man5/updatedb.conf.5*
%attr(0644,root,root) %{_mandir}/man8/updatedb.8*
%dir %{_sharedstatedir}/plocate
%attr(0644,root,root) %{_sharedstatedir}/plocate/CACHEDIR.TAG
%ghost %attr(0640,root,plocate) %verify(not md5 mtime) %{_sharedstatedir}/plocate/plocate.db
%license COPYING
%doc COPYING NEWS README



%changelog
* Sun May 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.rc4
- create the necessary group in %%pre scriptlet

* Sat May 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.rc3
- Don't install plocate-build

* Fri May 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.rc2
- update database via cron.hourly when at least 165 minutes old.

* Fri May 19 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.dev4
- correct permissions (I hope), cron job until systemd is in use

* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.18-0.dev1
- Initial spec file for YJL
- Need to setup perms/cronjob (cronjob until systemd)
