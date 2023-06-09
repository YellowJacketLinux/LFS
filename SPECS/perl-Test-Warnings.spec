%global cpanname Test-Warnings

%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global norequiremetacheck foo
%global norequirepadwalker bar
%endif
%endif

Name:     perl-%{cpanname}
Version:  0.031
Release:  %{?repo}0.rc2%{?dist}
Summary:  Test for warnings and the lack of them
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Test::Warnings
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(if)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# suggests
%if 0%{!?norequiremetacheck:1} == 1
BuildRequires:  perl(CPAN::Meta::Check) >= 0.011
%endif
BuildRequires:  perl(CPAN::Meta::Requirements)
%if 0%{!?norequirepadwalker:1} == 1
BuildRequires:  perl(PadWalker)
%endif
BuildRequires:  perl(Test::Tester) >= 0.108
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(Test::Builder)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
If you've ever tried to use Test::NoWarnings to confirm there are no
warnings generated by your tests, combined with the convenience of
done_testing to not have to declare a test count, you'll have discovered
that these two features do not play well together, as the test count
will be calculated before the warnings test is run, resulting in a TAP
error.

This module is intended to be used as a drop-in replacement for
Test::NoWarnings: it also adds an extra test, but runs this test before
done_testing calculates the test count, rather than after. It does this
by hooking into done_testing as well as via an END block. You can declare
a plan, or not, and things will still Just Work.

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


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Test
%attr(0444,root,root) %{perl5_vendorlib}/Test/Warnings.pm
%attr(0644,root,root) %{_mandir}/man3/Test::Warnings.3*
%license LICENCE
%doc CONTRIBUTING Changes LICENCE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.031-0.rc2
- BuildRequire perl-devel
- Conditionally require some optional test dependencies
- Conditionally run tests
- Require %%perl5_API

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.031-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
