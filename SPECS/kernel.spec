# no stripping
%global debug_package %{nil}
%global __strip /bin/true
# kernel tags
%global kseries 6.1
%global krel 32
%global localktag genesis.1

Name:     kernel
Version:  %{kseries}.%{krel}
Release:  %{?repo}%{localktag}%{?dist}
Summary:  The Linux kernel

Group:    System Environment/Kernel
License:  GPL-2.0 WITH Linux-syscall-note
URL:      https://www.kernel.org
Source0:  https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
Source1:  config-%{version}-%{localktag}
Provides: linux-kernel = %{kseries}

#BuildRequires:	
#Requires:	

%description
This package contains the Linux kernel. You can not boot GNU/Linux
without a kernel.

%package modules
Summary:  Linux Kernel Modules
Group:    System Environment/Core
Requires: %{name} = %{version}-%{release}

%description modules
This package includes the Linux kernel modules. You *probably* can not
successfully boot your system without the proper kernel modules package
that matches the kernel.

%package doc
Summary:  Linux Kernel Documentation
Group:    Developer/Documentation
BuildArch:  noarch
Requires: %{name} = %{version}-%{release}

%description doc
This package contains the Linux kernel documentation.

%prep
%setup -n linux-%{version}
make mrproper
cp %{SOURCE1} ./.config


%build
make oldconfig
make %{?_smp_mflags}


%install
export INSTALL_MOD_PATH=%{buildroot}
make modules_install
rm -f %{buildroot}/lib/modules/%{version}-%{localktag}/build
rm -f %{buildroot}/lib/modules/%{version}-%{localktag}/source
install -D -m644 .config %{buildroot}/boot/config-%{version}-%{localktag}
install -m644 System.map %{buildroot}/boot/System.map-%{version}-%{localktag}
install -m644 arch/%{_arch}/boot/bzImage %{buildroot}/boot/vmlinuz-%{version}-%{localktag}

install -d %{buildroot}%{_datadir}/doc
cp -r Documentation %{buildroot}%{_datadir}/doc/linux-%{version}

%files
%defattr(-,root,root,-)
/boot/config-%{version}-%{localktag}
/boot/System.map-%{version}-%{localktag}
/boot/vmlinuz-%{version}-%{localktag}
%license COPYING LICENSES
%doc COPYING CREDITS LICENSES MAINTAINERS README

%files modules
%defattr(-,root,root,-)
/lib/modules/%{version}-%{localktag}
%license COPYING LICENSES
%doc COPYING CREDITS LICENSES MAINTAINERS README

%files doc
%defattr(-,root,root,-)
%{_datadir}/doc/linux-%{version}


%changelog
* Mon Jun 05 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.32-genesis.1
- Update to 6.1.32

* Tue May 30 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.31-genesis.1
- Update to 6.1.31

* Wed May 24 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.30-genesis.1
- Update to 6.1.30

* Thu May 18 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.29-genesis.1
- Update to 6.1.29

* Thu May 11 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.28-genesis.1
- Update to 6.1.28
- Prune changelog

* Mon May 01 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.27-genesis.1
- Update to 6.1.27

* Thu Apr 27 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.26-genesis.1
- Update to 6.1.26

* Sat Mar 11 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.18-genesis.1
- Initial kernel packaging
