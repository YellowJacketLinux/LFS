%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed
%endif

%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     coreutils
Version:  9.1
Release:  %{?repo}0.rc4%{?dist}
Summary:  GNU core utilities

Group:    System Environment/Base
License:  GPL-3.0-or-later
URL:      https://www.gnu.org/software/coreutils/
Source0:  https://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz

BuildRequires:  %{__sed}
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(gmp)
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
The GNU Core Utilities are the basic file, shell and text manipulation
utilities of the GNU operating system. These are the core utilities which are
expected to exist on every operating system.

%prep
%setup -q


%build
%configure \
  --with-openssl=yes \
  --enable-no-install-program=kill,uptime
make %{?_smp_mflags}

%check
# fixme - one test failure:
# FAIL: tests/misc/stty-pairs.sh
%if 0%{?runtests:1} == 1
make RUN_EXPENSIVE_TESTS=yes check > coreutils-make-check.log 2>&1 ||:
%else
echo "make check not run at package build." > coreutils-make-check.log
%endif

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}
install -m755 -d %{buildroot}%{_sbindir}
install -m755 -d %{buildroot}%{_mandir}/man8
mv %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}/
%{__sed} -i 's/"1"/"8"/' %{buildroot}%{_mandir}/man1/chroot.1
mv %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
install -m755 -d %{buildroot}/bin
for file in cat chgrp chmod chown cp date dd df echo false ln ls mkdir mknod mv pwd rm rmdir stty sync true; do
  mv %{buildroot}%{_bindir}/${file} %{buildroot}/bin/
done

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /bin/*
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/chroot
%dir %{_libexecdir}/%{name}
%attr(0755,root,root) %{_libexecdir}/%{name}/libstdbuf.so
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/%{name}.info*
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man8/chroot.8*
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%doc coreutils-make-check.log


%changelog
* Sun May 21 2023 Michael A. Peters <anymouseprophet@gmail.com> 9.1-0.rc4
- LibreSSL build needs "--with-openssl=yes" specified

* Thu May 11 2023 Michael A. Peters <anymouseprophet@gmail.com> 9.1-0.rc2
- minor spec file tweaks.

* Tue Mar 14 2023 Michael A. Peters <anymouseprophet@gmail.com> 9.1-0.rc1
- Initial spec file
