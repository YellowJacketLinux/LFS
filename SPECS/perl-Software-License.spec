%global cpanname Software-License
%global licensedir %{_datadir}/licenses-cpan-common

Name:     perl-%{cpanname}
Version:  0.104002
Release:  %{?repo}0.dev1%{?dist}
Summary:  packages that provide templated software licenses
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later and Artistic-1.0-Perl
URL:      https://metacpan.org/dist/Software-License
Source0:  https://cpan.metacpan.org/authors/id/L/LE/LEONT/Software-License-0.104002.tar.gz
### AGPL
Source21: AGPL-3.0.txt
### Apache
Source22: Apache-1.1.txt
Source23: Apache-2.0.txt
### Artistic
Source24: Artistic-1.0-Perl.txt
Source25: Artistic-2.0.txt
### BSD
Source26: BSD-3-Clause.txt
### CC0
Source27: CC0-1.0.txt
### EUPL
Source28: EUPL-1.1.txt
Source29: EUPL-1.2.txt
### FreeBSD
Source30: BSD-2-Clause.txt
### GFDL
Source31: GFDL-1.2.txt
Source32: GFDL-1.3.txt
### GPL
Source33: GPL-1.0.txt
Source34: GPL-2.0.txt
Source35: GPL-3.0.txt
### ISC
Source36: ISC.txt
# LGPL
Source37: LGPL-2.1.txt
Source38: LGPL-3.0.txt
# MIT
Source39: MIT.txt
# Mozilla
Source40: MPL-1.0.txt
Source41: MPL-1.1.txt
Source42: MPL-2.0.txt
# both OpenSSL and SSLeay
Source43: OpenSSL.txt
Source44: SSLeay.txt
# Perl 5
Source45: Perl5-License.txt
### PostgreSQL
Source46: PostgreSQL.txt
### QPL
Source47: QPL-1.0.txt
### Zlib
Source49: Zlib.txt

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.78
# for test
BuildRequires:  perl(Test::More) perl(warnings)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Section)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Dir)
BuildRequires:  perl(Module::Load)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(Text::Template)
# runtime
Requires: perl(Carp)
Requires: perl(Data::Section)
Requires: perl(Text::Template)
Requires: perl(File::Spec)
Requires: perl(IO::Dir)
Requires: perl(Module::Load)
Requires: perl(parent)
Requires: perl(strict)
Requires: perl(utf8)
Requires: perl(warnings)
# keep the two packages in sync
Requires: common-CPAN-licenses = %{version}-%{release}

%description
This package provides templated software licenses.

%package -n common-CPAN-licenses
Summary:  License files commonly used in CPAN modules
Group:    Legal/Licenses
License:  Not-Applicable

%description -n common-CPAN-licenses
This package contains the text format version of license files for
software licenses that are likely to be encountered in packages on
the Comprehensive Perl Archive Network.

This package is provided as a convenience for the handful of cases
where a CPAN module specifies a license but does not include the text
of the license in the module source.


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

install -m755 -d %{buildroot}%{licensedir}
cat > %{buildroot}%{licensedir}/README.txt << "EOF"
A handful of perl modules on CPAN specify a license but do not actually
include a LICENSE or COPYING file with the text of the license.

In such cases, there is a good chance you can find the text of the
license within one of the sub-directories here.

The directories are named using the conventions of the Software::License
perl module (e.g. FreeBSD for the BSD 2-Clause license) but uses
the SPDX version 3 identifier for the name of the licence file.

EOF

#AGPL
install -m755 -d %{buildroot}%{licensedir}/AGPL
cat > %{buildroot}%{licensedir}/AGPL/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The official source for this license file, also available in other
file formats and lanuages, is:

    https://www.gnu.org/licenses/licenses.html

EOF
install -m644 %{SOURCE21} %{buildroot}%{licensedir}/AGPL/

#Apache
install -m755 -d %{buildroot}%{licensedir}/Apache
cat > %{buildroot}%{licensedir}/Apache/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files is:

    https://www.apache.org/licenses/

EOF
install -m644 %{SOURCE22} %{buildroot}%{licensedir}/Apache/
install -m644 %{SOURCE23} %{buildroot}%{licensedir}/Apache/

#Artistic
install -m755 -d %{buildroot}%{licensedir}/Artistic
cat > %{buildroot}%{licensedir}/Artistic/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files is:

    https://www.perlfoundation.org/artistic-license-10.html

    https://www.perlfoundation.org/artistic-license-20.html

There are three commonly found versions of the Artistic 1.0 license.
The version here is the version that is found in the Perl source
tarball.

It should be noted that many Free Libre Open Source Software experts
and projects do not consider the Artistic 1.0 license to be a free
software license and only consider software licensed with the Artistic
1.0 license to be "FLOSS" if it is dual-licensed with another license
that is a free software license (such as a GPL license).

The Artistic 2.0 license however is generally considered to be a free
software license.

EOF
install -m644 %{SOURCE24} %{buildroot}%{licensedir}/Artistic/
install -m644 %{SOURCE25} %{buildroot}%{licensedir}/Artistic/

#BSD
install -m755 -d %{buildroot}%{licensedir}/BSD
cat > %{buildroot}%{licensedir}/BSD/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/bsd-3-clause/

There are several variations of the BSD-3-Clause license. The variation
here is the variation from the above website.

EOF
install -m644 %{SOURCE26} %{buildroot}%{licensedir}/BSD/

#CC0
install -m755 -d %{buildroot}%{licensedir}/CC0
cat > %{buildroot}%{licensedir}/CC0/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The official source for this license file is:

    https://creativecommons.org/share-your-work/public-domain/cc0/

EOF
install -m644 %{SOURCE27} %{buildroot}%{licensedir}/CC0/

#EUPL
install -m755 -d %{buildroot}%{licensedir}/EUPL
cat > %{buildroot}%{licensedir}/EUPL/README.txt << "EOF"
The text format of these licenses are provided for your convenience.
For official information on the EUPL, please see:

    https://commission.europa.eu/content/european-union-public-licence_en

For both PDF and text versions of the 1.2 version in multiple languages,
please see:

    https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12

EOF
install -m644 %{SOURCE28} %{buildroot}%{licensedir}/EUPL/
install -m644 %{SOURCE29} %{buildroot}%{licensedir}/EUPL/

#FreeBSD
install -m755 -d %{buildroot}%{licensedir}/FreeBSD
cat > %{buildroot}%{licensedir}/FreeBSD/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/bsd-2-clause/

There are several variations of the BSD-2-Clause license. The variation
here is the variation from the above website.

EOF
install -m644 %{SOURCE30} %{buildroot}%{licensedir}/FreeBSD/

#GFDL
install -m755 -d %{buildroot}%{licensedir}/GFDL
cat > %{buildroot}%{licensedir}/GFDL/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files, also available in other
file formats and lanuages, is:

    https://www.gnu.org/licenses/licenses.html

EOF
install -m644 %{SOURCE31} %{buildroot}%{licensedir}/GFDL/
install -m644 %{SOURCE32} %{buildroot}%{licensedir}/GFDL/

#GPL
install -m755 -d %{buildroot}%{licensedir}/GPL
cat > %{buildroot}%{licensedir}/GPL/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files, also available in other
file formats and lanuages, is:

    https://www.gnu.org/licenses/licenses.html

EOF
install -m644 %{SOURCE33} %{buildroot}%{licensedir}/GPL/
install -m644 %{SOURCE34} %{buildroot}%{licensedir}/GPL/
install -m644 %{SOURCE35} %{buildroot}%{licensedir}/GPL/

#ISC
install -m755 -d %{buildroot}%{licensedir}/ISC
cat > %{buildroot}%{licensedir}/ISC/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/isc-license-txt/

EOF
install -m644 %{SOURCE36} %{buildroot}%{licensedir}/ISC/

#LGPL
install -m755 -d %{buildroot}%{licensedir}/LGPL
cat > %{buildroot}%{licensedir}/LGPL/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files, also available in other
file formats and lanuages, is:

    https://www.gnu.org/licenses/licenses.html

EOF
install -m644 %{SOURCE37} %{buildroot}%{licensedir}/LGPL/
install -m644 %{SOURCE38} %{buildroot}%{licensedir}/LGPL/

#MIT
install -m755 -d %{buildroot}%{licensedir}/MIT
cat > %{buildroot}%{licensedir}/MIT/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/mit/

EOF
install -m644 %{SOURCE39} %{buildroot}%{licensedir}/MIT/

#MPL
install -m755 -d %{buildroot}%{licensedir}/MPL
cat > %{buildroot}%{licensedir}/MPL/README.txt << "EOF"
The text format of these license files are provided for your convenience.
The official source for these license files is:

    https://www.mozilla.org/en-US/MPL/

EOF
install -m644 %{SOURCE40} %{buildroot}%{licensedir}/MPL/
install -m644 %{SOURCE41} %{buildroot}%{licensedir}/MPL/
install -m644 %{SOURCE42} %{buildroot}%{licensedir}/MPL/

#OpenSSL
install -m755 -d %{buildroot}%{licensedir}/OpenSSL
cat > %{buildroot}%{licensedir}/OpenSSL/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The official source for the license can be found at:

    https://www.openssl.org/source/license.html

EOF
install -m644 %{SOURCE43} %{buildroot}%{licensedir}/OpenSSL/

#SSLeay
install -m755 -d %{buildroot}%{licensedir}/SSLeay
cat > %{buildroot}%{licensedir}/SSLeay/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The official source for the license can be found at:

    https://www.openssl.org/source/license.html

EOF
install -m644 %{SOURCE44} %{buildroot}%{licensedir}/SSLeay/

#Perl5
install -m755 -d %{buildroot}%{licensedir}/Perl5
cat > %{buildroot}%{licensedir}/Perl5/README.txt << "EOF"
There is technically no such thing as a "Perl 5" license. However many
Perl modules simply state they are licensed under the same terms as
Perl 5 itself.

Perl 5 is dual-licensed Artistic-1.0-Perl and GPL-1.0.

The text format of these license files are provided for your convenience
along with the portion of the Pearl 5 README file that specifies the
dual license for Perl 5.

More information on Perl licensing can be found at:

    https://dev.perl.org/licenses/

EOF
install -m644 %{SOURCE45} %{buildroot}%{licensedir}/Perl5/
install -m644 %{SOURCE24} %{buildroot}%{licensedir}/Perl5/
install -m644 %{SOURCE33} %{buildroot}%{licensedir}/Perl5/

#PostgreSQL
install -m755 -d %{buildroot}%{licensedir}/PostgreSQL
cat > %{buildroot}%{licensedir}/PostgreSQL/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The official source for the license can be found at:

    https://www.postgresql.org/about/licence/

EOF
install -m644 %{SOURCE46} %{buildroot}%{licensedir}/PostgreSQL/

#QPL
install -m755 -d %{buildroot}%{licensedir}/QPL
cat > %{buildroot}%{licensedir}/QPL/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/qpl-1.0/

It should be noted that many Free Libre Open Source Software experts
and projects do not consider the QPL 1.0 license to be a free software
license and only consider software licensed with the QPL 1.0 license
to be "FLOSS" if it is dual-licensed with another license that is a
free software license (such as a GPL license).

EOF
install -m644 %{SOURCE47} %{buildroot}%{licensedir}/QPL/

#Zlib
install -m755 -d %{buildroot}%{licensedir}/Zlib
cat > %{buildroot}%{licensedir}/Zlib/README.txt << "EOF"
The text format of this license file is provided for your convenience.
The Open Source Initiative web page for this license:

    https://opensource.org/license/zlib-license-php/

EOF
install -m644 %{SOURCE49} %{buildroot}%{licensedir}/Zlib/


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Software
%attr(0444,root,root) %{perl5_vendorlib}/Software/License.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/LicenseUtils.pm
%dir %{perl5_vendorlib}/Software/License
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Custom.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/None.pm
# Standard Licenses
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/AGPL_3.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Apache_1_1.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Apache_2_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Artistic_1_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Artistic_2_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/BSD.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/CC0_1_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/EUPL_1_1.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/EUPL_1_2.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/FreeBSD.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/GFDL_1_2.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/GFDL_1_3.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/GPL_1.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/GPL_2.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/GPL_3.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/ISC.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/LGPL_2_1.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/LGPL_3_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/MIT.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Mozilla_1_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Mozilla_1_1.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Mozilla_2_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/OpenSSL.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/SSLeay.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Perl_5.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/PostgreSQL.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/QPL_1_0.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Sun.pm
%attr(0444,root,root) %{perl5_vendorlib}/Software/License/Zlib.pm
# man files
%attr(0644,root,root) %{_mandir}/man3/Software::License.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Custom.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::None.3*
%attr(0644,root,root) %{_mandir}/man3/Software::LicenseUtils.3*
# Standard Licenses
%attr(0644,root,root) %{_mandir}/man3/Software::License::AGPL_3.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Apache_1_1.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Apache_2_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Artistic_1_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Artistic_2_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::BSD.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::CC0_1_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::EUPL_1_1.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::EUPL_1_2.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::FreeBSD.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::GFDL_1_2.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::GFDL_1_3.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::GPL_1.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::GPL_2.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::GPL_3.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::ISC.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::LGPL_2_1.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::LGPL_3_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::MIT.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Mozilla_1_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Mozilla_1_1.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Mozilla_2_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::OpenSSL.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::SSLeay.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Perl_5.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::PostgreSQL.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::QPL_1_0.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Sun.3*
%attr(0644,root,root) %{_mandir}/man3/Software::License::Zlib.3*
# meta
%license LICENSE
%doc %{name}-make.test.log
%doc Changes LICENSE README

%files -n common-CPAN-licenses
%defattr(-,root,root,-)
%dir %{licensedir}
%attr(0644,root,root) %{licensedir}/README.txt
# Source 21
%dir %{licensedir}/AGPL
%attr(0644,root,root) %{licensedir}/AGPL/README.txt
%attr(0644,root,root) %{licensedir}/AGPL/AGPL-3.0.txt
# Source 22,23
%dir %{licensedir}/Apache
%attr(0644,root,root) %{licensedir}/Apache/README.txt
%attr(0644,root,root) %{licensedir}/Apache/Apache-1.1.txt
%attr(0644,root,root) %{licensedir}/Apache/Apache-2.0.txt
# Source 24,25
%dir %{licensedir}/Artistic
%attr(0644,root,root) %{licensedir}/Artistic/README.txt
%attr(0644,root,root) %{licensedir}/Artistic/Artistic-1.0-Perl.txt
%attr(0644,root,root) %{licensedir}/Artistic/Artistic-2.0.txt
# Source 26
%dir %{licensedir}/BSD
%attr(0644,root,root) %{licensedir}/BSD/README.txt
%attr(0644,root,root) %{licensedir}/BSD/BSD-3-Clause.txt
# Source 27
%dir %{licensedir}/CC0
%attr(0644,root,root) %{licensedir}/CC0/README.txt
%attr(0644,root,root) %{licensedir}/CC0/CC0-1.0.txt
# Source 28,29
%dir %{licensedir}/EUPL
%attr(0644,root,root) %{licensedir}/EUPL/README.txt
%attr(0644,root,root) %{licensedir}/EUPL/EUPL-1.1.txt
%attr(0644,root,root) %{licensedir}/EUPL/EUPL-1.2.txt
# Source 30
%dir %{licensedir}/FreeBSD
%attr(0644,root,root) %{licensedir}/FreeBSD/README.txt
%attr(0644,root,root) %{licensedir}/FreeBSD/BSD-2-Clause.txt
# Source 31,32
%dir %{licensedir}/GFDL
%attr(0644,root,root) %{licensedir}/GFDL/README.txt
%attr(0644,root,root) %{licensedir}/GFDL/GFDL-1.2.txt
%attr(0644,root,root) %{licensedir}/GFDL/GFDL-1.3.txt
# Source 33,34,35
%dir %{licensedir}/GPL
%attr(0644,root,root) %{licensedir}/GPL/README.txt
%attr(0644,root,root) %{licensedir}/GPL/GPL-1.0.txt
%attr(0644,root,root) %{licensedir}/GPL/GPL-2.0.txt
%attr(0644,root,root) %{licensedir}/GPL/GPL-3.0.txt
# Source 36
%dir %{licensedir}/ISC
%attr(0644,root,root) %{licensedir}/ISC/README.txt
%attr(0644,root,root) %{licensedir}/ISC/ISC.txt
# Source 37,38
%dir %{licensedir}/LGPL
%attr(0644,root,root) %{licensedir}/LGPL/README.txt
%attr(0644,root,root) %{licensedir}/LGPL/LGPL-2.1.txt
%attr(0644,root,root) %{licensedir}/LGPL/LGPL-3.0.txt
# Source 39
%dir %{licensedir}/MIT
%attr(0644,root,root) %{licensedir}/MIT/README.txt
%attr(0644,root,root) %{licensedir}/MIT/MIT.txt
# Source 40,41,42
%dir %{licensedir}/MPL
%attr(0644,root,root) %{licensedir}/MPL/README.txt
%attr(0644,root,root) %{licensedir}/MPL/MPL-1.0.txt
%attr(0644,root,root) %{licensedir}/MPL/MPL-1.1.txt
%attr(0644,root,root) %{licensedir}/MPL/MPL-2.0.txt
# Source 43
%dir %{licensedir}/OpenSSL
%attr(0644,root,root) %{licensedir}/OpenSSL/README.txt
%attr(0644,root,root) %{licensedir}/OpenSSL/OpenSSL.txt
# Source 44
%dir %{licensedir}/SSLeay
%attr(0644,root,root) %{licensedir}/SSLeay/README.txt
%attr(0644,root,root) %{licensedir}/SSLeay/SSLeay.txt
# Source 45 24 33
%dir %{licensedir}/Perl5
%attr(0644,root,root) %{licensedir}/Perl5/README.txt
%attr(0644,root,root) %{licensedir}/Perl5/Perl5-License.txt
%attr(0644,root,root) %{licensedir}/Perl5/Artistic-1.0-Perl.txt
%attr(0644,root,root) %{licensedir}/Perl5/GPL-1.0.txt
# Source46
%dir %{licensedir}/PostgreSQL
%attr(0644,root,root) %{licensedir}/PostgreSQL/README.txt
%attr(0644,root,root) %{licensedir}/PostgreSQL/PostgreSQL.txt
# Source47
%dir %{licensedir}/QPL
%attr(0644,root,root) %{licensedir}/QPL/README.txt
%attr(0644,root,root) %{licensedir}/QPL/QPL-1.0.txt
# Source48
# Source49
%dir %{licensedir}/Zlib
%attr(0644,root,root) %{licensedir}/Zlib/README.txt
%attr(0644,root,root) %{licensedir}/Zlib/Zlib.txt

%changelog
* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.104002-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
