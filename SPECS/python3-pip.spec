%global gittag 23.1.2

Name:     python3-pip
Version:  %{gittag}
Release:  %{?repo}0.rc2%{?dist}
Summary:  Package Installer for Python
BuildArch:  noarch

Group:    Development/Python
License:  MIT
URL:      https://pip.pypa.io/en/stable/
Source0:  https://github.com/pypa/pip/archive/refs/tags/%{gittag}.tar.gz

BuildRequires:  python3-devel
Requires: python3-devel
Requires: make-ca
%if 0%{?python3_API:1} == 1
# Non-Standard Macro
Requires: %{python3_API}
%endif

%description
pip is the package installer for Python. You can use it to install
packages from the Python Package Index and other indexes.

%prep
%setup -q -n pip-%{gittag}


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

# PIP3 certs
[ ! -d %{buildroot}%{_sysconfdir}/profile.d ] && mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cat > %{buildroot}%{_sysconfdir}/profile.d/pythoncerts.sh << "EOF"
# Begin /etc/profile.d/pythoncerts.sh

export _PIP_STANDALONE_CERT=/etc/pki/tls/certs/ca-bundle.crt

# End /etc/profile.d/pythoncerts.sh
EOF

cat > %{buildroot}%{_sysconfdir}/pip.conf << EOF
[global]
require-virtualenv = true
disable-pip-version-check = true
EOF

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/pip
%attr(0755,root,root) %{_bindir}/pip3
%attr(0755,root,root) %{_bindir}/pip3.11
%dir %{python3_sitelib}/pip
%attr(0644,root,root) %{python3_sitelib}/pip/*.py
%attr(0644,root,root) %{python3_sitelib}/pip/py.typed
%{python3_sitelib}/pip/_internal
%{python3_sitelib}/pip/_vendor
%{python3_sitelib}/pip/__pycache__
%{python3_sitelib}/pip-%{gittag}-py%{python3_version}.egg-info
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pip.conf
%attr(0644,root,root) %{_sysconfdir}/profile.d/pythoncerts.sh
%license LICENSE.txt
%doc AUTHORS.txt LICENSE.txt NEWS.rst README.rst SECURITY.md docs/html
%doc %{name}-setup.py.test.log



%changelog
* Thu May 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 23.1.2-0.rc2
- changes to pip.conf file

* Wed May 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 23.1.2-0.rc1
- Initial spec file for YJL.
