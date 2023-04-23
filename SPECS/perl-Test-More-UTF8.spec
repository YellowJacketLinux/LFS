%global cpanname Test-More-UTF8

Name:     perl-%{cpanname}
Version:  0.05
Release:  %{?repo}0.rc2%{?dist}
Summary:  Enhancing Test::More for UTF8-based projects
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later and Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Test::More::UTF8
Source0:  https://cpan.metacpan.org/authors/id/M/MO/MONS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) perl(warnings)
BuildRequires:  perl(Test::More)
%endif
# Runtime
Requires: perl(Test::More)
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Test::More::UTF8 - Enhancing Test::More for UTF8-based projects.

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

%if 0%{?perl5_cpanlic:1} == 1
cat > Perl5-Licenses.txt << "EOF"
This package specifies it uses the Perl 5 licenses but did not include
them in the package source.

They can be found in the following directory:

  %{perl5_cpanlic}/Perl5/

EOF
%endif

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Test
%dir %{perl5_vendorlib}/Test/More
%attr(0444,root,root) %{perl5_vendorlib}/Test/More/UTF8.pm
%attr(0644,root,root) %{_mandir}/man3/Test::More::UTF8.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt
%doc Changes README Perl5-Licenses.txt
%else
%doc Changes README
%endif
%doc %{name}-make.test.log



%changelog
* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.05-0.rc2
- Fix license issue, conditional run tests, add API requirement.

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.05-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
