%global cpanname Data-Section

Name:     perl-%{cpanname}
Version:  0.200008
Release:  %{?repo}0.rc2%{?dist}
Summary:  read multiple hunks of data out of your DATA section
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later and Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Data-Section
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::FailWarnings)
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Encode)
BuildRequires:  perl(MRO::Compat) >= 0.09
BuildRequires:  perl(Sub::Exporter) >= 0.979
BuildRequires:  perl(strict)
%endif
# Runtime
Requires: perl(Encode)
Requires: perl(MRO::Compat) >= 0.09
Requires: perl(Sub::Exporter) >= 0.979
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Data::Section - read multiple hunks of data out of your DATA section

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
%attr(0444,root,root) %{perl5_vendorlib}/Data/Section.pm
%attr(0644,root,root) %{_mandir}/man3/Data::Section.3*
%license LICENSE
%doc %{name}-make.test.log
%doc Changes LICENSE README



%changelog
* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.200008-0.rc2
- Require %%perl5_API, conditionally run tests.

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.200008-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
