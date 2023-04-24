%global cpanname Try-Tiny

Name:     perl-%{cpanname}
Version:  0.31
Release:  %{?repo}0.rc2%{?dist}
Summary:  Minimal try/catch module

Group:    Development/Libraries
License:  MIT
URL:      https://metacpan.org/pod/Try::Tiny
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(CPAN::Meta)
#BuildRequires:  perl(CPAN::Meta::Check)
BuildRequires:  perl(CPAN::Meta::Requirements)
%endif
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This module provides bare bones try/catch/finally statements that are
designed to minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch which provides a nice syntax and avoids adding
another call stack layer, and supports calling return from the try block
to return from the parent subroutine. These extra features come at a
cost of a few dependencies, namely Devel::Declare and Scope::Upper which
are occasionally problematic, and the additional catch filtering uses
Moose type constraints which may not be desirable either.

The main focus of this module is to provide simple and reliable error
handling for those having a hard time installing TryCatch, but who still
want to write correct eval blocks without 5 lines of boilerplate each
time.

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
%dir %{perl5_vendorlib}/Try
%attr(0444,root,root) %{perl5_vendorlib}/Try/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Try::Tiny.3*
%license LICENCE
%doc LICENCE Changes
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.31-0.rc2
- BuildRequire perl-devel
- Conditionally run tests
- Require %%perl5_API

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.31-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
