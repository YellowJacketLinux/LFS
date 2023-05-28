%global gitv 0.1.0

Name:     yjl-sysusers
Version:  %{gitv}
Release:	1%{?dist}
Summary:  utility for adding system groups and users
BuildArch:  noarch

Group:    System Administration/Utilities
License:  MIT
URL:      https://github.com/YellowJacketLinux/%{name}
Source0:  https://github.com/YellowJacketLinux/%{name}/archive/refs/tags/v0.1.0.tar.gz

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

%build
# If a distribution specific JSON exists in contrib, then
# cat contrib/whatever.json > yjl-sysusers.json

%install
make install PYTHON=%{python3} RPMMACRODIR=%{_rpmmacrodir} DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%attr(0750,root,root) %{_sbindir}/yjl-sysusers
%dir %{_datadir}/yjl-sysusers
%attr(0444,root,root) %{_datadir}/yjl-sysusers/yjl-sysusers.json
%attr(0644,root,root) %{_rpmmacrodir}/macros.yjl-sysusers
%attr(0644,root,root) %{_mandir}/man5/yjl-sysusers.json.5*
%attr(0644,root,root) %{_mandir}/man8/yjl-sysusers.8*
%license LICENSE
%doc CHARITYWARE.md LICENSE README.md TODO.md YJL-Notes.md yjl-sysusers.json

%changelog
* Sun May 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.1.0-1
- Initial reference spec file

