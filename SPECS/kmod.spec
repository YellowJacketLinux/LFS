Name:     kmod
Version:  30
Release:  %{?repo}0.rc2%{?dist}
Summary:  Utilities for loading kernel modules

Group:    System Environment/Kernel
License:  GPL-2.0-or-later
URL:      https://github.com/kmod-project/kmod
Source0:  https://www.kernel.org/pub/linux/utils/kernel/kmod/kmod-30.tar.xz

BuildRequires:  liblzma-devel libzstd-devel zlib-devel
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
Requires: libkmod = %{version}-%{release}

%description
kmod is a set of tools to handle common tasks with Linux kernel modules
like insert, remove, list, check properties, resolve dependencies and
aliases.

These tools are designed on top of libkmod, a library that is shipped
with kmod. See /usr/share/doc/libkmod-%{version}/README for more details
on this library and how to use it. The aim is to be compatible with
tools, configurations and indexes from module-init-tools project.

%package -n libkmod
Group:    System Environment/Libraries
Summary:  A shared library used for kernel module purposes

%description -n libkmod
libkmod was created to allow programs to easily insert, remove and
list modules, also checking its properties, dependencies and aliases.

%package -n libkmod-devel
Group:    Development/Libraries
Summary:  Developer files for libkmod
License:  LGPL-2.1-or-later
Requires: libkmod = %{version}-%{release}
Provides: kmod-devel

%description -n libkmod-devel
This package contains the library header files needed to compile software
that links against the libkmod library.

%prep
%setup -q


%build
%configure \
  --libdir=/%{_lib} \
  --bindir=/bin \
  --with-openssl \
  --with-xz \
  --with-zstd \
  --with-zlib
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

# adjust pkgconfig
sed -i 's?libdir=.*?libs=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/libkmod.pc
install -d %{buildroot}%{_libdir}
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}/
ln -s ../../%{_lib}/libkmod.so.2.4.0 %{buildroot}%{_libdir}/libkmod.so
rm -f %{buildroot}/%{_lib}/libkmod.so

# symlinks
install -d %{buildroot}/sbin
ln -s ../bin/kmod %{buildroot}/sbin/depmod
ln -s ../bin/kmod %{buildroot}/sbin/insmod
ln -s ../bin/kmod %{buildroot}/sbin/modinfo
ln -s ../bin/kmod %{buildroot}/sbin/modprobe
ln -s ../bin/kmod %{buildroot}/sbin/rmmod

ln -s kmod %{buildroot}/bin/lsmod

%post -n libkmod -p /sbin/ldconfig
%postun -n libkmod -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/bin/*
/sbin/*
%{_datadir}/bash-completion/completions/kmod
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%license COPYING
%doc README.md tools/COPYING NEWS TODO

%files -n libkmod
%defattr(-,root,root,-)
/%{_lib}/libkmod.so.2
%attr(0755,root,root) /%{_lib}/libkmod.so.2.4.0
%license libkmod/COPYING
%doc libkmod/README libkmod/COPYING

%files -n libkmod-devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/libkmod.h
%{_libdir}/libkmod.so
%attr(0644,root,root) %{_libdir}/pkgconfig/libkmod.pc
%license libkmod/COPYING
%doc libkmod/README libkmod/COPYING

%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> 30-0.rc2
- Better %%description for libkmod (from the README)

* Sun Mar 19 2023 Michael A. Peters <anymouseprophet@gmail.com> 30-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
