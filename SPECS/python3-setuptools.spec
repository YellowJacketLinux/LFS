%global dnlhash e5d7ae40d03e4ed20b7cba317cf9c0c97097c8debb39f9d72d182a6578a2

Name:     python3-setuptools
Version:  67.7.2
Release:  %{?repo}0.rc1%{?dist}
Summary:  build, install, upgrade, and uninstall Python packages
BuildArch:  noarch

Group:    Development/Python
License:  MIT
URL:      https://pypi.org/project/setuptools/
Source0:  https://files.pythonhosted.org/packages/fd/53/%{dnlhash}/setuptools-%{version}.tar.gz

BuildRequires:  python3-devel
Requires: python3-pip

%description
This package is used for installing, upgrading, and uninstalling python
packages.

%prep
%setup -q -n setuptools-%{version}


%build
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py build --executable="%{python3} -s"


%check
%if 0%{?runtestsBROKEN:1} == 1
%{python3} setup.py test > %{name}-setup.py.test.log 2>&1
%else
echo "setup.py test not run during package build" > %{name}-setup.py.test.log
%endif


%install
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py install -O1 --skip-build --root %{buildroot}


%files
%defattr(-,root,root,-)
%{python3_sitelib}/setuptools
%{python3_sitelib}/setuptools-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/pkg_resources
%{python3_sitelib}/_distutils_hack
%attr(0644,root,root) %{python3_sitelib}/distutils-precedence.pth
%license LICENSE
%doc CHANGES.rst LICENSE README.rst docs



%changelog
* Wed May 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 67.7.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
