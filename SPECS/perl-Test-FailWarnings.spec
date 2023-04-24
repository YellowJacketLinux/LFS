%global cpanname Test-FailWarnings

Name:     perl-%{cpanname}
Version:  0.008
Release:  %{?repo}0.rc2%{?dist}
Summary:  Add test failures if warnings are caught
BuildArch:  noarch

Group:    Development/Libraries
License:  Apache-2.0
URL:      https://metacpan.org/pod/Test::FailWarnings
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(Capture::Tiny) >= 0.12
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(strict)
%endif
# Runtime
Requires: perl(Carp)
Requires: perl(Cwd)
Requires: perl(File::Spec)
Requires: perl(Test::More) >= 0.96
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This module hooks $SIG{__WARN__} and converts warnings to Test::More
fail() calls. It is designed to be used with done_testing, when you
don't need to know the test count in advance.

Just as with Test::NoWarnings, this does not catch warnings if other
things localize $SIG{__WARN__}, as this is designed to catch unhandled
warnings.

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
%attr(0444,root,root) %{perl5_vendorlib}/Test/FailWarnings.pm
%attr(0644,root,root) %{_mandir}/man3/Test::FailWarnings.3*
%license LICENSE
%doc CONTRIBUTING Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.008-0.rc3
- BuildRequires perl-devel
- Conditionally run tests, require %%perl5_API

* Fri Apr 21 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.008-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
