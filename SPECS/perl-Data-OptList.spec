%global cpanname Data-OptList

Name:     perl-%{cpanname}
Version:  0.113
Release:  %{?repo}0.rc3%{?dist}
Summary:  Parse and validate simple name/value option pairs
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Data-OptList
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
BuildRequires:  perl(JSON::PP) >= 2.27300
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Params::Util)
BuildRequires:  perl(Sub::Install) >= 0.921
BuildRequires:  perl(strict)
%endif
# Runtime
Requires: perl(List::Util)
Requires: perl(Params::Util)
Requires: perl(Sub::Install) >= 0.921
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Data::OptList - parse and validate simple name/value option pairs.

%prep
%setup -n %{cpanname}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make test > %{name}-make.test.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.test.log
%endif

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}%{perl5_vendorlib}


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Data
%attr(0444,root,root) %{perl5_vendorlib}/Data/OptList.pm
%attr(0644,root,root) %{_mandir}/man3/Data::OptList.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.113-0.rc3
- BuildRequire perl-devel

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.113-0.rc2
- Require %%perl5_API and conditionally run test suite.

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.113-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
