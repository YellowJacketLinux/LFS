%global cpanname Mozilla-CA

Name:     perl-%{cpanname}
Version:  20221114
Release:  %{?repo}0.rc1%{?dist}
Summary:  Mozilla's CA cert bundle in PEM format
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl and MPL-2.0
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/H/HA/HAARG/%{cpanname}-%{version}.tar.gz
Patch0:   Mozilla-CA-20221114-cacert.patch

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Spec)
%endif
# runtime
Requires: perl(File::Spec)
# /end runtime
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif

%description
Mozilla::CA provides a copy of Mozilla's bundle of Certificate Authority
certificates in a form that can be consumed by modules and libraries
based on OpenSSL.

The module provide a single function: SSL_ca_file()

It returns the absolute path to the Mozilla's CA cert bundle PEM file.


%prep
%setup -n %{cpanname}-%{version}
%patch 0 -p1


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

The bundled certificate file falls under the Mozilla Public License 2.0
and can be found in the following directory:

  %{perl5_cpanlic}/MPL/

EOF
%endif

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Mozilla
%attr(0444,root,root) %{perl5_vendorlib}/Mozilla/CA.pm
%dir %{perl5_vendorlib}/Mozilla/CA
%attr(0444,root,root) %{perl5_vendorlib}/Mozilla/CA/cacert.pem
%attr(0644,root,root) %{_mandir}/man3/Mozilla::CA.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt
%doc Changes README Perl5-Licenses.txt
%else
%doc Changes README
%endif
%doc %{name}-make.test.log



%changelog
* Sat May 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 20221114-0.rc1
- Initial RPM spec file for YJL
