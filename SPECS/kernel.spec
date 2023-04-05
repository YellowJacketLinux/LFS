# no stripping
%define debug_package %{nil}
%define __strip /bin/true
# kernel tags
%define kseries 6.1
%define krel 22
%define localktag genesis.1

Name:		kernel
Version:	%{kseries}.%{krel}
Release:	%{?repo}%{localktag}%{?dist}
Summary:	The Linux kernel

Group:		System Environment/Core
License:	GPLv2
URL:		https://www.kernel.org
Source0:	https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
Source1:	config-%{version}-%{localktag}
Provides:	linux-kernel = %{kseries}

#BuildRequires:	
#Requires:	

%description
This package contains the Linux kernel. You can not boot GNU/Linux without a
kernel.

%package modules
Summary:	Linux Kernel Modules
Group:		System Environment/Core
Requires:	%{name} = %{version}-%{release}

%description modules
This package includes the Linux kernel modules. You *probably* can not
successfully boot your system without the proper kernel modules package
that matches the kernel.

%package doc
Summary:	Linux Kernel Documentation
Group:		Developer/Documentation
BuildArch:	noarch
Requires:	%{name} = %{version}-%{release}

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
%doc COPYING CREDITS LICENSES MAINTAINERS README

%files modules
%defattr(-,root,root,-)
/lib/modules/%{version}-%{localktag}
%doc COPYING CREDITS LICENSES MAINTAINERS README

%files doc
%defattr(-,root,root,-)
%{_datadir}/doc/linux-%{version}


%changelog
* Mon Apr 03 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.22-genesis.1
- Update to 6.1.22

* Wed Mar 22 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.21-genesis.1
- Update to 6.1.21

* Fri Mar 17 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.20-genesis.1
- Update to 6.1.20 kernel, split off modules into a subpackage, make the
- documentation package a noarch package.

* Tue Mar 14 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.19-genesis.1
- Update to 6.1.19 kernel

* Sat Mar 11 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.18-genesis.1
- Initial kernel packaging
