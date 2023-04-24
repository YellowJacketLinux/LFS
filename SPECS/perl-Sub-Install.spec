%global cpanname Sub-Install

Name:     perl-%{cpanname}
Version:  0.929
Release:  %{?repo}0.rc3%{?dist}
Summary:  Install subroutines into packages easily
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Sub-Install
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(B)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
%endif
# Runtime
Requires: perl(B)
Requires: perl(Carp)
Requires: perl(Scalar::Util)
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This module makes it easy to install subroutines into packages without
the unsightly mess of no strict or typeglobs lying about where just
anyone can see them.

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
%dir %{perl5_vendorlib}/Sub
%attr(0444,root,root) %{perl5_vendorlib}/Sub/Install.pm
%attr(0644,root,root) %{_mandir}/man3/Sub::Install.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.929-0.rc3
- BuildRequires perl-devel
- Conditionally run tests, require %%perl5_API

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.929-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
