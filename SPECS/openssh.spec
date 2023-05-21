%global specrel 0.rc2

# ssh-keygen -A
# no init script yet - blfs-bootscripts make install-sshd

%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
# disable these features for 1.core. build
%global nopam      foo
%global nokerberos bar
%global nolibedit  foobar
%endif
%endif

%if 0%{?__install:1}
%global __install %{_bindir}/install
%endif
# for tests
%if 0%{?!__scp:1}
%global __scp %{_bindir}/scp
%endif

Name:     openssh	
Version:  9.3p1
Release:  %{?repo}%{specrel}%{?dist}
Summary:  Secure Shell

Group:    System Environment/Utilities
License:  BSD-2-Clause, BSD-3-Clause, ISC-style, and MIT-style
URL:      https://www.openssh.com/
Source0:  https://ftp.usa.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz

%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
%if 0%{?!nopam:1} == 1
BuildRequires:  pam-devel
%endif
%if 0%{?!nokerberos:1} == 1
BuildRequires:  kerberos5-devel
%endif
%if 0%{?!nolibedit:1} == 1
BuildRequires:  libedit-devel
%endif
%if 0%{?runtests:1} == 1
BuildRequires:  gdb
BuildRequires:  %{__scp}
%endif
BuildRequires:  pkgconfig(zlib)
BuildRequires:  %{__install}
### These add entropy, extra entropy is never bad but I do not think they
### are necessary as of kernel 5.6 series.
#Requires: net-tools sysstat
#Requires: haveged

%description
OpenSSH is the premier connectivity tool for remote login with the SSH
protocol. It encrypts all traffic to eliminate eavesdropping, connection
hijacking, and other attacks. In addition, OpenSSH provides a large suite
of secure tunneling capabilities, several authentication methods, and
sophisticated configuration options.

%package clients
Group:    System Environment/Utilities
Summary:  OpenSSH clients
Requires: %{name} = %{version}-%{release}

%description clients
This package contains the OpenSSH clients: list

%package server
Group:    System Environment/Daemons
Summary:  OpenSSH server
Requires: %{name} = %{version}-%{release}

%description server
This package contains the OpenSSH server daemon.

%prep
%setup -q


%build
%configure \
  --sysconfdir=/etc/ssh                    \
  --with-privsep-path=/var/lib/sshd        \
  --with-default-path=/usr/bin:/bin        \
  --with-superuser-path=/usr/sbin:/usr/bin:/sbin:/bin \
%if 0%{?!nopam:1} == 1
  --with-pam                               \
%endif
%if 0%{?!nokerberos} == 1
  --with-kerberos5=%{_prefix}              \
%endif
%if 0%{?!nolibet} == 1
  --with-libedit                           \
%endif
  --with-xauth=%{_bindir}/xauth            \
  --with-pid-dir=/run
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
echo "PermitRootLogin no" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
%__install -m755 contrib/ssh-copy-id %{buildroot}%{_bindir}/
%__install -m644 contrib/ssh-copy-id.1 %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sharedstatedir}/sshd

%if 0%{?!nopam:1} == 1
mkdir -p %{buildroot}%{_sysconfdir}/pam.d/sshd
# do stuff to make etc/pam.d/sshd
echo "UsePAM yes" >> %{buildroot}%{_sysconfdir}/ssh/sshd_config
%endif

%check
%if 0%{?runtests:1} == 1
TEST_SSH_UNSAFE_PERMISSIONS=1 \
make -j1 tests > %{name}-make.tests.log 2>&1
%else
echo "tests not run during package build" > %{name}-make.tests.log
%endif


%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(4711,root,root) %{_libexecdir}/ssh-keysign
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md
%doc %{name}-make.tests.log

%files clients
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/scp
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_libexecdir}/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/ssh-sk-helper
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%attr(0644,root,root) %{_mandir}/man8/ssh-sk-helper.8*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md

%files server
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%if 0%{?!nopam:1} == 1
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/sshd
%endif
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/sftp-server
%attr(0700,root,sys) %dir %{_sharedstatedir}/sshd
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%license LICENCE
%doc CREDITS LICENCE OVERVIEW PROTOCOL* README* SECURITY.md

%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.3p1-0.rc2
- Rebuild with correct %%{_sharedstatedir} macro

* Fri May 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.3p1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
