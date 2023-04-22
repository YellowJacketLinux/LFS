%global cpanname MRO-Compat

Name:     perl-%{cpanname}
Version:  0.15
Release:  %{?repo}0.rc1%{?dist}
Summary:  mro::* interface compatibility for Perls < 5.9.5
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later and Artistic-1.0-Perl
URL:      https://metacpan.org/pod/MRO::Compat
Source0:  https://cpan.metacpan.org/authors/id/H/HA/HAARG/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
BuildRequires:  perl(Test::More) perl(warnings)

%description
The "mro" namespace provides several utilities for dealing with method
resolution order and method caching in general in Perl 5.9.5 and higher.

This module provides those interfaces for earlier versions of Perl (back
to 5.6.0 anyways).

It is a harmless no-op to use this module on 5.9.5+. That is to say,
code which properly uses MRO::Compat will work unmodified on both older
Perls and 5.9.5+.

If you're writing a piece of software that would like to use the parts
of 5.9.5+'s mro:: interfaces that are supported here, and you want
compatibility with older Perls, this is the module for you.

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
%dir %{perl5_vendorlib}/MRO
%attr(0444,root,root) %{perl5_vendorlib}/MRO/Compat.pm
%attr(0644,root,root) %{_mandir}/man3/MRO::Compat.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Fri Apr 21 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.15-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
