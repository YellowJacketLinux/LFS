%global cpanname Text-Template

Name:     perl-%{cpanname}
Version:  1.61
Release:  %{?repo}0.rc2%{?dist}
Summary:  Expand template text with embedded Perl
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Text::Template
Source0:  https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Test::More::UTF8)
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(lib)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Encode)
Requires: perl(Exporter)
Requires: perl(base)
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This is a library for generating form letters, building HTML pages, or
filling in templates generally. A `template' is a piece of text that
has little Perl programs embedded in it here and there. When you
`fill in' a template, you evaluate the little programs and replace them
with their values.

You can store a template in a file outside your program. People can
modify the template without modifying the program. You can separate the
formatting details from the main code, and put the formatting parts of
the program into the template. That prevents code bloat and encourages
functional separation.

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
%dir %{perl5_vendorlib}/Text
%attr(0444,root,root) %{perl5_vendorlib}/Text/Template.pm
%dir %{perl5_vendorlib}/Text/Template
%attr(0444,root,root) %{perl5_vendorlib}/Text/Template/Preprocess.pm
%{_mandir}/man3/Text::Template.3*
%{_mandir}/man3/Text::Template::Preprocess.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.61-0.rc2
- BuildRequire perl-devel
- Conditionally run tests
- Require %%perl5_API

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.61-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
