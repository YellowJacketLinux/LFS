%global cpanname Test-Needs

Name:     perl-%{cpanname}
Version:  0.002010
Release:  %{?repo}0.rc1%{?dist}
Summary:  Skip tests when modules not available
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Test-Needs
Source0:  https://cpan.metacpan.org/authors/id/H/HA/HAARG/Test-Needs-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
%endif
# runtime
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Skip test scripts if modules are not available. The requested modules
will be loaded, and optionally have their versions checked. If the
module is missing, the test script will be skipped. Modules that are
found but fail to compile will exit with an error rather than skip.



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
%attr(0444,root,root) %{perl5_vendorlib}/Test/Needs.pm
%attr(0644,root,root) %{_mandir}/man3/Test::Needs.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Fri Apr 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.002010-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
