Name:     meson
Version:  1.1.0
Release:	%{?repo}0.rc1%{?dist}
Summary:  fast build system
BuildArch:  noarch

Group:    Development/Utilities
License:  Apache-2.0
URL:      https://mesonbuild.com/
Source0:  https://github.com/mesonbuild/meson/releases/download/%{version}/meson-%{version}.tar.gz

BuildRequires:  python3-devel
Requires: ninja
Requires: python3-%{name} = %{version}-%{release}

%description
Meson is an open source build system meant to be both extremely fast,
and, even more importantly, as user friendly as possible.

The main design point of Meson is that every moment a developer spends
writing or debugging build definitions is a second wasted. So is every
second spent waiting for the build system to actually start compiling
code.

%package -n python3-%{name}
Group:    Development/Libraries
Summary:  Meson build system Python bindings
Requires: %{name} = %{version}-%{release}
%if 0%{?python3_API:1} == 1
# Non-Standard Macro
Requires: %{python3_API}
%endif

%description -n python3-%{name}
This package contains the Python3 component of the Meson build system.

%prep
%setup -q


%build
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py build --executable="%{python3} -s"


%install
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py install -O1 --skip-build --root %{buildroot}

install -Dm644 data/shell-completions/bash/meson %{buildroot}%{_datadir}/bash-completion/completions/meson
install -vDm644 data/shell-completions/zsh/_meson %{buildroot}%{_datadir}/zsh/site-functions/_meson


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/meson
%attr(0644,root,root) %{_datadir}/bash-completion/completions/meson
%attr(0644,root,root) %{_datadir}/zsh/site-functions/_meson
%attr(0644,root,root) %{_datadir}/polkit-1/actions/com.mesonbuild.install.policy
%attr(0644,root,root) %{_mandir}/man1/meson.1*
%license COPYING
%doc contributing.md COPYING README.md

%files -n python3-%{name}
%defattr(-,root,root,-)
%{python3_sitelib}/mesonbuild
%{python3_sitelib}/meson-%{version}-py%{python3_version}.egg-info
%license COPYING
%doc contributing.md COPYING README.md


%changelog
* Thu May 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.1.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
