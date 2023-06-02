%global gitv 0.1.5

Name:     yjl-sysusers
Version:  %{gitv}
Release:  1%{?dist}
Summary:  utility for adding system groups and users
BuildArch:  noarch

Group:    System Administration/Utilities
License:  MIT
URL:      https://github.com/YellowJacketLinux/%{name}
Source0:  https://github.com/YellowJacketLinux/%{name}/archive/refs/tags/v%{gitv}.tar.gz

BuildRequires:  python3-devel
Requires:       python3

%description
yjl-sysusers is a wrapper script to the operating system groupadd (8)
and useradd (8) commands that allows respecting the operating system
static UID and GID assignment when available, without the need to assign
them manually.

Static UID and GID values, as well as some other parameters useful to
the useradd (8) command, are defined in the file yjl-sysusers.json (5)
which is normally located in the directory /usr/share/yjl-sysusers.

yjl-sysusers was developed with RPM package scriptlets in mind.

%prep
%setup -q
# set shebang to full path
sed -i 's?/usr/bin/env python3?%{python3}?' functions.py

%build
# If a distribution specific JSON exists in contrib, then
# cat contrib/whatever.json > yjl-sysusers.json

%install
PYTHON=%{python3} RPMMACRODIR=%{_rpmmacrodir} DESTDIR=%{buildroot} \
make install-rpm
# Adjust README.md for %%doc
sed -i '/For installation instructions/d' README.md
sed -i '/justsayno.jpg/d' README.md
sed -i '5d' README.md
sed -i 's?docs/yjl?yjl?g' README.md

%files
%defattr(-,root,root,-)
%attr(0750,root,root) %{_sbindir}/yjl-sysusers
%dir %{_datadir}/yjl-sysusers
%attr(0644,root,root) %{_datadir}/yjl-sysusers/yjl-sysusers.json
%attr(0644,root,root) %{_rpmmacrodir}/macros.yjl-sysusers
%attr(0644,root,root) %{_mandir}/man5/yjl-sysusers.json.5*
%attr(0644,root,root) %{_mandir}/man8/yjl-sysusers.8*
%license LICENSE
%doc CHARITYWARE.md LICENSE README.md yjl-sysusers.json
%doc docs/yjl-sysusers.json.5.md docs/yjl-sysusers.8.md
%doc YJL-Notes.md

%changelog
* Fri Jun 02 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.1.5-1
- Update to 0.1.5

* Sun May 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.1.0-1
- Reference spec file

