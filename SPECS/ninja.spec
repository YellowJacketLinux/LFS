Name:     ninja
Version:  1.11.1
Release:	%{?repo}0.rc1%{?dist}
Summary:  small build system with a focus on speed

Group:    Development/Utilities
License:  Apache-2.0
URL:      https://ninja-build.org/
Source0:  https://github.com/ninja-build/ninja/archive/v%{version}/ninja-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  libstdc++-devel
#Requires:	

%description
Ninja is a small build system with a focus on speed. It differs from
other build systems in two major respects: it is designed to have its
input files generated by a higher-level build system, and it is designed
to run builds as fast as possible.

%prep
%setup -q
sed -i '/int Guess/a \
  int   j = 0;\
  char* jobs = getenv( "NINJAJOBS" );\
  if ( jobs != NULL ) j = atoi( jobs );\
  if ( j > 0 ) return j;\
' src/ninja.cc


%build
%{python3} configure.py --bootstrap


%check
%if 0%{?runtests:1} == 1
./ninja ninja_test
./ninja_test --gtest_filter=-SubprocessTest.SetWithLots
%endif


%install
install -Dm755 ninja %{buildroot}%{_bindir}/ninja
install -Dm644 misc/bash-completion %{buildroot}%{_datadir}/bash-completion/completions/ninja
install -Dm644 misc/zsh-completion %{buildroot}%{_datadir}/zsh/site-functions/_ninja


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/ninja
%attr(0644,root,root) %{_datadir}/bash-completion/completions/ninja
%attr(0644,root,root) %{_datadir}/zsh/site-functions/_ninja
%license COPYING
%doc CONTRIBUTING.md COPYING README.md doc



%changelog
* Wed May 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.11.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
