%global githubv 20230430

Name:     make-ca
Version:  %{githubv}
Release:  %{?repo}0.rc1%{?dist}
Summary:  Manage PKI configuration
BuildArch:  noarch

Group:		System Environment/Utilities
License:  MIT and GPL-3.0-only
URL:      https://github.com/YellowJacketLinux/make-ca
Source0:  https://github.com/YellowJacketLinux/make-ca/archive/refs/tags/%{githubv}.tar.gz

Requires: libressl
Requires: curl
Requires: nss
Requires: p11-kit
Requires(post): libressl
Requires(post): nss
Requires(post): p11-kit

%description
make-ca is a utility to deliver and manage a complete PKI configuration
for workstations and servers using only standard Unix utilities, LibreSSL,
curl, and p11-kit, using a Mozilla cacerts.txt or like file as the trust
source. It can optionally generate keystores for OpenJDK PKCS#12 and
NSS if installed.

make-ca was originally developed for use with Linux From Scratch to
minimize dependencies for early system build, but has been written to
be generic enough for any Linux distribution. This version has been
modified for YellowJacket GNU/Linux (YJL).


%prep
%setup -q -n make-ca-%{version}


%build


%install
make install DESTDIR=%{buildroot}

%post
if [ $1 == 1 ]; then
%{_sbindir}/make-ca -f -C %{_sysconfdir}/make-ca/certdata-dist.txt \
  > /dev/null 2>&1 ||:
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/make-ca
%attr(0644,root,root) %{_sysconfdir}/make-ca/CS.txt
%attr(0644,root,root) %{_sysconfdir}/make-ca/certdata-dist.txt
%attr(0644,root,root) %{_sysconfdir}/make-ca/make-ca.conf.dist
#%%attr(0644,root,root) %%{_prefix}/lib/systemd/system/update-pki.service
#%%attr(0644,root,root) %%{_prefix}/lib/systemd/system/update-pki.timer
%dir %{_libexecdir}/make-ca
%attr(0700,root,root) %{_libexecdir}/make-ca/copy-trust-modifications
%attr(0755,root,root) %{_sbindir}/make-ca
%attr(0644,root,root) %{_mandir}/man8/make-ca.8*
%license LICENSE LICENSE.GPLv3 LICENSE.MIT LICENSE.MPLv2
%doc CHANGELOG* README.md LICENSE LICENSE.GPLv3 LICENSE.MIT LICENSE.MPLv2



%changelog
* Sun Apr 30 2023 Michael A. Peters <anymouseprophet@gmail.com> - 20230430-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
