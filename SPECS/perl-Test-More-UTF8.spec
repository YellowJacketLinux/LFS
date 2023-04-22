%global cpanname Test-More-UTF8

Name:     perl-%{cpanname}
Version:  0.05
Release:  %{?repo}0.rc1%{?dist}
Summary:  Enhancing Test::More for UTF8-based projects
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later and Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Test::More::UTF8
Source0:  https://cpan.metacpan.org/authors/id/M/MO/MONS/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
BuildRequires:  perl(Test::More) perl(warnings)
BuildRequires:  perl(Test::More)
# Runtime
Requires: perl(Test::More)

%description
Test::More::UTF8 - Enhancing Test::More for UTF8-based projects.

%prep
%setup -n %{cpanname}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%check
make test > %{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}%{perl5_vendorlib}


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Test
%dir %{perl5_vendorlib}/Test/More
%attr(0444,root,root) %{perl5_vendorlib}/Test/More/UTF8.pm
%attr(0644,root,root) %{_mandir}/man3/Test::More::UTF8.3*
%doc Changes README
%doc %{name}-make.test.log



%changelog
* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.05-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
