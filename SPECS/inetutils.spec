%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     inetutils
Version:  2.4
Release:  %{?repo}0.rc2%{?dist}
Summary:  Some programs for basic networking

Group:		Network/Utilities
License:	GPLv3
URL:      https://www.gnu.org/software/inetutils/
Source0:  https://ftp.gnu.org/gnu/inetutils/%{name}-%{version}.tar.xz

BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
#Requires:
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
Inetutils is a collection of common network programs. This package
includes dnsdomainname, ftp, hostname, ifconfig, ping, ping6, talk,
telnet, tftp, and traceroute.

The YJL packaging of inetutils does __not__ contain inetutils builds
of logger, whois, the various inetutils servers, or the dangerous
and obsolete rtools.

%prep
%setup -q


%build
%configure \
  --disable-logger     \
  --disable-whois      \
  --disable-rcp        \
  --disable-rexec      \
  --disable-rlogin     \
  --disable-rsh        \
  --disable-servers
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
install -m755 -d %{buildroot}/bin
install -m755 -d %{buildroot}/sbin
mv %{buildroot}%{_bindir}/hostname %{buildroot}/bin/
mv %{buildroot}%{_bindir}/ifconfig %{buildroot}/sbin/
 
%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) /bin/hostname
%attr(0755,root,root) /sbin/ifconfig
%attr(0755,root,root) %{_bindir}/dnsdomainname
%attr(0755,root,root) %{_bindir}/ftp
%attr(0755,root,root) %{_bindir}/ping
%attr(0755,root,root) %{_bindir}/ping6
%attr(0755,root,root) %{_bindir}/talk
%attr(0755,root,root) %{_bindir}/telnet
%attr(0755,root,root) %{_bindir}/tftp
%attr(0755,root,root) %{_bindir}/traceroute
%attr(0644,root,root) %{_infodir}/%{name}.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/*.1*
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS ChangeLog* COPYING NEWS README THANKS TODO


%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.4-0.rc2
- Use %%{insinfo}, add some missing BuildRequires

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
