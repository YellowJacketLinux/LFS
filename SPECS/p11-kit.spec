# FIXME - bash-completion missing

Name:     p11-kit
Version:  0.24.1
Release:	1%{?dist}
Summary:  load and enumerate PKCS#11 modules

Group:    System Environment/Utilities
License:  BSD-3-Clause
URL:      https://p11-glue.github.io/p11-glue/p11-kit.html
Source0:  https://github.com/p11-glue/p11-kit/releases/download/%{version}/p11-kit-%{version}.tar.xz
Patch0:   p11-kit-0.24.1-trust.patch

BuildRequires:  libffi-devel
BuildRequires:  libtasn1-devel
BuildRequires:  libxslt-devel
BuildRequires:  meson
BuildRequires:  ninja
Requires: nss
Requires: make-ca
Requires: %{name}-libs = %{version}-%{release}

%description
p11-kit provides a way to load and enumerate PKCS#11 modules. It provides
a standard configuration setup for installing PKCS#11 modules in such
a way that they are discoverable.

%package libs
Group:    System Environment/Libraries
Summary:  %{name} shared libraries

%description libs
This package containst the %{name} shared libraries.

%package devel
Group:    Development/Libraries
Summary:  Development files for %{name}
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains the developer files necessary to compile software
that links against the %{name} libraries.

%prep
%setup -q
%patch 0 -p1


%build
mkdir p11-build
cd p11-build

meson --prefix=%{_prefix} \
      --buildtype=release \
      -Dtrust_paths=/etc/pki/anchors

ninja


%check
cd p11-build
ninja test > %{name}-ninja.test.log 2>&1


%install
cd p11-build
DESTDIR=%{buildroot} ninja install
%find_lang %{name}
ln -sf ../libexec/p11-kit/trust-extract-compat \
  %{buildroot}%{_bindir}/update-ca-certificates

ln -sf ./pkcs11/p11-kit-trust.so %{buildroot}%{_libdir}/libnssckbi.so

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f p11-build/%{name}.lang
%defattr(-,root,root,-)
%dir %{_sysconfdir}/pkcs11
%attr(0644,root,root) %{_sysconfdir}/pkcs11/pkcs11.conf.example
%attr(0755,root,root) %{_bindir}/p11-kit
%attr(0755,root,root) %{_bindir}/trust
%{_bindir}/update-ca-certificates
%dir %{_libexecdir}/p11-kit
%attr(0755,root,root) %{_libexecdir}/p11-kit/p11-kit-remote
%attr(0755,root,root) %{_libexecdir}/p11-kit/p11-kit-server
%attr(0755,root,root) %{_libexecdir}/p11-kit/trust-extract-compat
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%attr(0644,root,root) %{_datadir}/p11-kit/modules/p11-kit-trust.module
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README
%doc p11-build/%{name}-ninja.test.log

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libp11-kit.so.0.3.0
%{_libdir}/libp11-kit.so.0
%{_libdir}/libnssckbi.so
%{_libdir}/p11-kit-proxy.so
%dir %{_libdir}/pkcs11
%attr(0755,root,root) %{_libdir}/pkcs11/p11-kit-client.so
%attr(0755,root,root) %{_libdir}/pkcs11/p11-kit-trust.so
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/p11-kit-1
%dir %{_includedir}/p11-kit-1/p11-kit
%attr(0644,root,root) %{_includedir}/p11-kit-1/p11-kit/*.h
%{_libdir}/libp11-kit.so
%attr(0644,root,root) %{_libdir}/pkgconfig/p11-kit-1.pc
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README

%changelog
* Mon May 1 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.24.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
