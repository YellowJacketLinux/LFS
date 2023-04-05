Name:		kernel-abi-headers
Version:	6.1.14
Release:	2%{?dist}
Summary:	The Linux Kernel ABI Headers for GLibC

Group:		Development/Libraries
License:	GPLv2
URL:		https://www.kernel.org
Source0:	https://www.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
BuildArch:	noarch
Provides:	kernel-headers = %{version}

%description
These are the Linux kernel headers that glibc builds against. The version
of the kernel these headers are from does not need to match the version
of the running kernel and should NOT be upgraded.

%prep
%setup -n linux-%{version}

%build
make mrproper
make headers
find usr/include -type f ! -name '*.h' -delete

%install
mkdir -p %{buildroot}%{_prefix}
cp -ar usr/include %{buildroot}%{_prefix}/

%files
%defattr(-,root,root,-)
%{_includedir}/asm
%{_includedir}/asm-generic
%{_includedir}/drm
%{_includedir}/linux
%{_includedir}/misc
%{_includedir}/mtd
%{_includedir}/rdma
%{_includedir}/scsi
%{_includedir}/sound
%{_includedir}/video
%{_includedir}/xen
%license COPYING
%doc COPYING CREDITS

%changelog
* Tue Mar 14 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.14-2
- Renamed from kernel-headers to kernel-abi-headers to avoid confusion.

* Sat Mar 11 2023 Michael A. Peters <anymouseprohet@gmail.com> - 6.1.14-1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
