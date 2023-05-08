# WARNING - init script not added

# blfs bootscriptd: make install-ntpd

%global pkgv 4.2.8
%global uppatch p15
%global upstreamV %{pkgv}%{uppatch}
%global specrel %{uppatch}.%{?repo}0.rc1%{?dist}

%global _bindir %{_sbindir}

Name:     ntp
Version:  %{pkgv}
Release:  %{specrel}
Summary:  Network Time Protocol RFC-5905 implementation

Group:    System Environment/Daemons
License:  ISC-like and BSD-2-Clause
URL:      https://www.eecis.udel.edu/~mills/ntp/html/
Source0:  https://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/ntp-%{upstreamV}.tar.gz
Source1:  ntp-conf

%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
BuildRequires:  libcap-devel
BuildRequires:  libevent-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  perl(IO::Socket::SSL)
Requires: perl(IO::Socket::SSL)
Requires: perl-NTP-Util = 0.77-%{release}

%description
This distribution is an implementation of RFC-5905 "Network Time Protocol
Version 4: Protocol and Algorithms Specification".

NTP is widely used to synchronize a computer to Internet time servers
or other sources, such as a radio or satellite receiver or telephone
modem service. It can also be used as a server for dependent clients.
It provides accuracies typically less than a millisecond on LANs and
up to a few milliseconds on WANs. Typical NTP configurations utilize
multiple redundant servers and diverse network paths in order to achieve
high accuracy and reliability.

%package -n perl-NTP-Util
Summary:  NTP Util perl modules
Group:    Development/Libraries
Version:  0.77
BuildArch:  noarch
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description -n perl-NTP-Util
This package includes the perl module distributed with the ntp package.

%prep
%setup -q -n %{name}-%{upstreamV}
sed -e 's/"(\\S+)"/"?([^\\s"]+)"?/' \
  -i scripts/update-leap/update-leap.in
sed -e 's/#ifndef __sun/#if !defined(__sun) \&\& !defined(__GLIBC__)/' \
  -i libntp/work_thread.c


%build
%configure \
  --enable-libuxcaps \
  --with-lineeditlibs=readline \
  --without-rpath

###RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fPIC"
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
[ ! -d %{buildroot}%{_sysconfdir} ] && mkdir -p %{buildroot}%{_sysconfdir}
install -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ntp.conf
install -d %{buildroot}%{_sharedstatedir}/ntp

install -d %{buildroot}%{perl5_vendorlib}/NTP
mv %{buildroot}%{_datadir}/ntp/lib/NTP/Util.pm %{buildroot}%{perl5_vendorlib}/NTP/

sed -i '/^use lib /d' %{buildroot}%{_sbindir}/ntp-wait
sed -i '/^use lib /d' %{buildroot}%{_sbindir}/ntptrace

mkdir pkgdoc
mv %{buildroot}%{_datadir}/doc/ntp pkgdoc/
mv %{buildroot}%{_datadir}/doc/sntp pkgdoc/

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_sbindir}/calc_tickadj
%attr(0755,root,root) %{_sbindir}/ntp-keygen
%attr(0755,root,root) %{_sbindir}/ntpd
%attr(0755,root,root) %{_sbindir}/ntpdate
%attr(0755,root,root) %{_sbindir}/ntpdc
%attr(0755,root,root) %{_sbindir}/ntpq
%attr(0755,root,root) %{_sbindir}/ntptime
%attr(0755,root,root) %{_sbindir}/ntptrace
%attr(0755,root,root) %{_sbindir}/ntp-wait
%attr(0755,root,root) %{_sbindir}/sntp
%attr(0755,root,root) %{_sbindir}/tickadj
%attr(0755,root,root) %{_sbindir}/update-leap
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ntp.conf
%attr(0755,ntp,ntp) %dir %{_sharedstatedir}/ntp
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man5/*.5*
%license COPYRIGHT
%doc ChangeLog NEWS README* COPYRIGHT
%doc pkgdoc/ntp/*.html pkgdoc/ntp/html pkgdoc/sntp

%files -n perl-NTP-Util
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/NTP
%attr(0444,root,root) %{perl5_vendorlib}/NTP/Util.pm
%license COPYRIGHT
%doc COPYRIGHT



%changelog
* Sat May 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.2.8-p15.0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
