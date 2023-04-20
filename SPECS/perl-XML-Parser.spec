%global cpanname XML-Parser

Name:     perl-%{cpanname}
Version:  2.46
Release:  %{?repo}0.rc1%{?dist}
Summary:  A perl module for parsing XML documents

Group:    Perl/Libraries
License:  GPL or Perl Artistic
URL:      https://metacpan.org/pod/XML::Parser
Source0:  https://cpan.metacpan.org/authors/id/T/TO/TODDR/%{cpanname}-%{version}.tar.gz

BuildRequires:  expat-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
BuildRequires:  perl(Test::More) perl(warnings)

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
make test > %{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}%{perl5_vendorarch}


%files
%defattr(-,root,root,-)
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
%doc %{name}-make.test.log
%doc README samples



%changelog
* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.46-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
