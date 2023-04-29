%global cpanname Test-Fatal

Name:     perl-%{cpanname}
Version:  0.017
Release:  %{?repo}0.rc1%{?dist}
Summary:  incredibly simple helpers for testing code with exceptions
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Test-Fatal
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.65
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(overload)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Try::Tiny) >= 0.07
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Exporter) >= 5.57
Requires: perl(Test::Builder)
Requires: perl(Try::Tiny) >= 0.07
Requires: perl(strict)
Requires: perl(warnings)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Test::Fatal is an alternative to the popular Test::Exception. It does
much less, but should allow greater flexibility in testing exception-
throwing code with about the same amount of typing.

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
%attr(0444,root,root) %{perl5_vendorlib}/Test/Fatal.pm
%attr(0644,root,root) %{_mandir}/man3/Test::Fatal.3*
%license LICENSE
%doc Changes LICENSE README examples
%doc %{name}-make.test.log



%changelog
* Fri Apr 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.017-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
