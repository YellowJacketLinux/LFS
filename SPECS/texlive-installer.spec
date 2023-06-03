Name:     texlive-installer
Version:  2023
Release:  %{?repo}0.rc4%{?dist}
Summary:  Helper script for installing TeXLive

Group:    Publishing
License:  CC0 Public Domain
URL:      https://github.com/YellowJacketLinux/LFS
Source0:  yjl-install-tl.sh
Source1:  profile.d-texlive.sh
Source2:  update-tl.sh
Source3:  CC0-Public_Domain.md
BuildArch:  noarch

BuildRequires:  yjl-sysusers
Requires: %{_sysconfdir}/profile
Requires: perl(Digest::MD5)
Requires(pre):  %{_yjl_sysusers}

%description
This package installs the script `yjl-install-tl.sh' and `update-tl.sh'
into %{_datadir}/doc/%{name}-%{version} and sets up the filesystem
to install TeXLive %{version}.

After installing this package, AS THE `texlive' user, run the script
`yjl-install-tl.sh' to install TeXLive. Then periodically, also AS THE
`texlive' user, run the script `update-tl.sh' to update TeXLive packages.

Any user who has been added to the group `texlive' will have TeXLive
in their executable path, along with the man pags and info pages.

Additional administration, such as setting the default paper size or
adding custom add-on packages and fonts, should be performed by the
`texlive' user.


%prep
%setup -n %{name}-%{version} -c -T
cp %{SOURCE0} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build

%install
install -m755 -d %{buildroot}%{_sysconfdir}/profile.d
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/texlive.sh
install -m755 -d %{buildroot}/opt/texlive/%{version}
install -m755 -d %{buildroot}/opt/texlive/texmf-local

%pre
%{_yjl_sysusers} --userandgroup \
  -d /opt/texlive/tladmin \
  -s /bin/bash --mkdir texlive

%files
%defattr(-,root,root,-)
%attr(0644,root,root) %{_sysconfdir}/profile.d/texlive.sh
%attr(0755,texlive,texlive) /opt/texlive/%{version}
%attr(0755,texlive,texlive) /opt/texlive/texmf-local
%license CC0-Public_Domain.md
%doc yjl-install-tl.sh update-tl.sh

%changelog
* Sat Jun 03 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2023-0.rc4
- Use yjl-sysusers to ensure user/group exist

* Sun May 21 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2023-0.rc3
- Added perl(Digest::MD5) to runtime Requires

* Tue Apr 04 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2023-0.rc2
- Update the /etc/profile.d/texlive.sh script so that /usr/local/bin
- and /usr/bin come before the texlive path.

* Wed Mar 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2023-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
