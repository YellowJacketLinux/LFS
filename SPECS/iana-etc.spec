Name:		iana-etc
Version:	20230330
Release:	1%{?dist}
Summary:	IANA Assigned Internet Protocol Numbers

Group:		System Environment/Base
License:	Distributable
URL:		https://github.com/Mic92/iana-etc
Source0:	https://github.com/Mic92/iana-etc/releases/download/%{version}/iana-etc-%{version}.tar.gz
BuildArch:	noarch

%description
A collection of IANA's Assigned Internet Protocol Numbers that is kept up to
date and conveniently packaged for Un*x package distribution.


%prep
%setup -q


%build

%install
install -m755 -d %{buildroot}%{_sysconfdir}
install -m644 protocols %{buildroot}%{_sysconfdir}/
install -m644 services  %{buildroot}%{_sysconfdir}/


%files
%defattr(-,root,root,-)
%attr(0644,root,root) %{_sysconfdir}/protocols
%attr(0644,root,root) %{_sysconfdir}/services



%changelog
* Thu Apr 06 2023 Michael A. Peters <anymousepropget@gmail.com> - 20230330-1
- Update to 20230330 release

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 20230316-1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
