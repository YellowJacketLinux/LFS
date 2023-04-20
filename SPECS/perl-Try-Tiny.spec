%global cpanname Try-Tiny

Name:     perl-%{cpanname}
Version:  0.31
Release:  %{?repo}0.rc1%{?dist}
Summary:  Minimal try/catch module

Group:    Development/Libraries
License:  MIT
URL:      https://metacpan.org/pod/Try::Tiny
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
BuildRequires:  perl(Test::More) perl(warnings)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(CPAN::Meta)
#BuildRequires:  perl(CPAN::Meta::Check)
BuildRequires:  perl(CPAN::Meta::Requirements)

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
make test > %{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}%{perl5_vendorlib}


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Try
%attr(0444,root,root) %{perl5_vendorlib}/Try/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Try::Tiny.3*
%license LICENCE
%doc LICENCE Changes
%doc %{name}-make.test.log



%changelog
* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.31-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
