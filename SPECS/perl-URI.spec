%global cpanname URI

Name:     perl-%{cpanname}
Version:  5.17
Release:  %{?repo}0.rc1%{?dist}
Summary:  Uniform Resource Identifiers (absolute and relative)
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/O/OA/OALDERS/URI-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(MIME::Base64) >= 2
BuildRequires:  perl(Net::Domain)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(constant)
BuildRequires:  perl(integer)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Business::ISBN) >= 3.005
BuildRequires:  perl(Regexp::IPv6) >= 0.03
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Cwd)
Requires: perl(Data::Dumper)
Requires: perl(Encode)
Requires: perl(Exporter) >= 5.57
Requires: perl(MIME::Base64) >= 2
Requires: perl(Net::Domain)
Requires: perl(Scalar::Util)
Requires: perl(constant)
Requires: perl(integer)
Requires: perl(overload)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(utf8)
Requires: perl(warnings)
Requires: perl(Business::ISBN) >= 3.005
Requires: perl(Regexp::IPv6) >= 0.03
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).

A Uniform Resource Identifier is a compact string of characters that
identifies an abstract or physical resource. A Uniform Resource
Identifier can be further classified as either a Uniform Resource Locator
(URL) or a Uniform Resource Name (URN). The distinction between URL and
URN does not matter to the URI class interface. A "URI-reference" is a
URI that may have additional information attached in the form of a
fragment identifier.

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
%attr(0444,root,root) %{perl5_vendorlib}/URI.pm
%dir %{perl5_vendorlib}/URI
%attr(0444,root,root) %{perl5_vendorlib}/URI/Escape.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/Heuristic.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/IRI.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/QueryParam.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/Split.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/URL.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/WithBase.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_foreign.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_generic.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_idna.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_ldap.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_login.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_punycode.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_query.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_segment.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_server.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/_userpass.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/data.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file.pm
%dir %{perl5_vendorlib}/URI/file
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/Base.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/FAT.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/Mac.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/OS2.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/QNX.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/Unix.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/file/Win32.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/ftp.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/gopher.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/http.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/https.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/ldap.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/ldapi.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/ldaps.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/mailto.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/mms.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/news.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/nntp.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/nntps.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/pop.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/rlogin.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/rsync.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/rtsp.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/rtspu.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/sftp.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/sip.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/sips.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/snews.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/ssh.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/telnet.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/tn3270.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/urn.pm
%dir %{perl5_vendorlib}/URI/urn
%attr(0444,root,root) %{perl5_vendorlib}/URI/urn/isbn.pm
%attr(0444,root,root) %{perl5_vendorlib}/URI/urn/oid.pm
%attr(0644,root,root) %{_mandir}/man3/URI.3*
%attr(0644,root,root) %{_mandir}/man3/URI::Escape.3*
%attr(0644,root,root) %{_mandir}/man3/URI::Heuristic.3*
%attr(0644,root,root) %{_mandir}/man3/URI::QueryParam.3*
%attr(0644,root,root) %{_mandir}/man3/URI::Split.3*
%attr(0644,root,root) %{_mandir}/man3/URI::URL.3*
%attr(0644,root,root) %{_mandir}/man3/URI::WithBase.3*
%attr(0644,root,root) %{_mandir}/man3/URI::_punycode.3*
%attr(0644,root,root) %{_mandir}/man3/URI::data.3*
%attr(0644,root,root) %{_mandir}/man3/URI::file.3*
%attr(0644,root,root) %{_mandir}/man3/URI::ldap.3*
%license LICENSE
%doc Changes CONTRIBUTING.md LICENSE README
%doc %{name}-make.test.log



%changelog
* Sat Apr 29 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.17-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
