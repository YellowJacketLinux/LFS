%global cpanname XML-Parser

%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global norequirelwp foo
%endif
%endif

Name:     perl-%{cpanname}
Version:  2.46
Release:  %{?repo}0.rc4%{?dist}
Summary:  A perl module for parsing XML documents

Group:    Perl/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/pod/XML::Parser
Source0:  https://cpan.metacpan.org/authors/id/T/TO/TODDR/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  expat-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(warnings)
%if 0%{!?norequirelwp:1} == 1
BuildRequires:  perl(LWP::UserAgent)
%endif
%endif
# runtime
%if 0%{!?norequirelwp:1} == 1
Requires: perl(LWP::UserAgent)
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif

%description
This module provides ways to parse XML documents. It is built on top
of XML::Parser::Expat, which is a lower level interface to James Clark's
expat library. Each call to one of the parsing methods creates a new
instance of XML::Parser::Expat which is then used to parse the document.
Expat options may be provided when the XML::Parser object is created.
These options are then passed on to the Expat object on each parse call.
They can also be given as extra arguments to the parse methods, in which
case they override options given at XML::Parser creation time.

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
%{_fixperms} %{buildroot}%{perl5_vendorarch}

%if 0%{?perl5_cpanlic:1} == 1
cat > Perl5-Licenses.txt << "EOF"
This package specifies it uses the Perl 5 licenses but did not include
them in the package source.

They can be found in the following directory:

  %{perl5_cpanlic}/Perl5/

EOF
%endif

%files
%dir %{perl5_vendorarch}/XML
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser.pm
%dir %{perl5_vendorarch}/XML/Parser
%dir %{perl5_vendorarch}/XML/Parser/Encodings
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/Japanese_Encodings.msg
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/README
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Encodings/*.enc
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Expat.pm
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/LWPExternEnt.pl
%dir %{perl5_vendorarch}/XML/Parser/Style
%attr(0444,root,root) %{perl5_vendorarch}/XML/Parser/Style/*.pm
%dir %{perl5_vendorarch}/auto/XML
%dir %{perl5_vendorarch}/auto/XML/Parser
%dir %{perl5_vendorarch}/auto/XML/Parser/Expat
%attr(0555,root,root) %{perl5_vendorarch}/auto/XML/Parser/Expat/Expat.so
# man files
%attr(0644,root,root) %{_mandir}/man3/*.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt
%doc Changes README samples Perl5-Licenses.txt
%else
%doc Changes README samples
%endif
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.46-0.rc4
- Make dependency on LWP::UserAgent conditional
- BuildRequire perl-devel

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.46-0.rc3
- Update how license is done, add ABI requirement

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.46-0.rc2
- License file

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.46-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
