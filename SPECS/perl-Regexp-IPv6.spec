%global cpanname Regexp-IPv6

Name:     perl-%{cpanname}
Version:  0.03
Release:  %{?repo}0.rc1%{?dist}
Summary:  Regular expression for IPv6 addresses
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SA/SALVA/Regexp-IPv6-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
%endif
# runtime
#Requires:
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif

%description
This module exports the $IPv6_re regular expression that matches any
valid IPv6 address as described in "RFC 2373 - 2.2 Text Representation
of Addresses" but ::. Any string not compliant with such RFC will be
rejected.

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
%dir %{perl5_vendorlib}/Regexp
%attr(0444,root,root) %{perl5_vendorlib}/Regexp/IPv6.pm
%attr(0644,root,root) %{_mandir}/man3/Regexp::IPv6.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt README
%doc Changes README Perl5-Licenses.txt
%else
%license README
%doc Changes README
%endif
%doc %{name}-make.test.log



%changelog
* Sat Apr 29 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.03-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
