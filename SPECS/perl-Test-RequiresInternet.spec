%global cpanname Test-RequiresInternet

Name:     perl-%{cpanname}
Version:  0.05
Release:  %{?repo}0.rc1%{?dist}
Summary:  Easily test network connectivity
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Test-RequiresInternet
Source0:  https://cpan.metacpan.org/authors/id/M/MA/MALLEN/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Socket)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%endif
# runtime
Requires: perl(Socket)
Requires: perl(strict)
Requires: perl(warnings)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This module is intended to easily test network connectivity before
functional tests begin to non-local Internet resources. It does not
require any modules beyond those supplied in core Perl.

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
%attr(0444,root,root) %{perl5_vendorlib}/Test/RequiresInternet.pm
%attr(0644,root,root) %{_mandir}/man3/Test::RequiresInternet.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Fri Apr 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.05-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
