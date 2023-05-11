%global dnlhash 0335f7217dd1e8096a9e8383e1d472aa14717878ffe07c4772e68b6e8735

%if 0%{?!__pip3:1} == 1
%global __pip3 %{_bindir}/pip3
%endif

Name:     python3-wheel
Version:  0.40.0
Release:  %{?repo}0.rc1%{?dist}
Summary:  Python wheel packaging standard 
BuildArch:  noarch

Group:    Development/Python
License:  MIT
URL:      https://github.com/pypa/wheel
Source0:  https://files.pythonhosted.org/packages/fc/ef/%{dnlhash}/wheel-%{version}.tar.gz

#BuildRequires:  %%{__pip3}
#Requires:
%if 0%{?python3_API:1} == 1
# Non-Standard Macro
Requires: %{python3_API}
%endif

%description
This library is the reference implementation of the Python wheel packaging
standard, as defined in PEP 427.

It has two different roles:

1) A setuptools extension for building wheels that provides the bdist_wheel
setuptools command.

2) A command line tool for working with wheel files.

It should be noted that wheel is not intended to be used as a library,
and as such there is no stable, public API.


%prep
%setup -q -n wheel-%{version}


%build
#PYTHONPATH=src %%{__pip3} wheel -w dist --no-build-isolation --no-deps $PWD
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py build --executable="%{python3} -s"


%install
#DESTDIR=%%{buildroot} %%{__pip3} install --no-index --find-links=dist wheel
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}" \
%{python3} setup.py install -O1 --skip-build --root %{buildroot}


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/wheel
%{python3_sitelib}/wheel
%{python3_sitelib}/wheel-%{version}-py%{python3_version}.egg-info
%license LICENSE.txt
%doc LICENSE.txt README.rst docs


%changelog
* Wed May 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.44-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
