%global cpanname Sub-Exporter

Name:     perl-%{cpanname}
Version:  0.989
Release:  %{?repo}0.rc3%{?dist}
Summary:  A sophisticated exporter for custom-built routines
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Sub::Exporter
Source0:  https://cpan.metacpan.org/authors/id/R/RJ/RJBS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(subs)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::OptList) >= 0.100
BuildRequires:  perl(Params::Util) >= 0.14
BuildRequires:  perl(Sub::Install) >= 0.92
BuildRequires:  perl(strict)
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Data::OptList) >= 0.100
Requires: perl(Params::Util) >= 0.14
Requires: perl(Sub::Install) >= 0.92
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
ACHTUNG! If you're not familiar with Exporter or exporting, read
Sub::Exporter::Tutorial first!

The biggest benefit of Sub::Exporter over existing exporters (including
the ubiquitous Exporter.pm) is its ability to build new coderefs for
export, rather than to simply export code identical to that found in
the exporting package.

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
%attr(0444,root,root) %{perl5_vendorlib}/Sub/Exporter.pm
%dir %{perl5_vendorlib}/Sub/Exporter
%attr(0444,root,root) %{perl5_vendorlib}/Sub/Exporter/Cookbook.pod
%attr(0444,root,root) %{perl5_vendorlib}/Sub/Exporter/Tutorial.pod
%attr(0444,root,root) %{perl5_vendorlib}/Sub/Exporter/Util.pm
%attr(0644,root,root) %{_mandir}/man3/Sub::Exporter.3*
%attr(0644,root,root) %{_mandir}/man3/Sub::Exporter::Cookbook.3*
%attr(0644,root,root) %{_mandir}/man3/Sub::Exporter::Tutorial.3*
%attr(0644,root,root) %{_mandir}/man3/Sub::Exporter::Util.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.989-0.rc3
- BuildRequires: perl-devel
- Conditionally run tests, require %%perl5_API

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.989-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
