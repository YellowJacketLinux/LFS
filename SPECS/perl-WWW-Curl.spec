%global cpanname WWW-Curl

Name:     perl-%{cpanname}
Version:  4.17
Release:  %{?repo}0.rc1%{?dist}
Summary:  Perl extension interface for libcurl
#BuildArch:  noarch

Group:    Development/Libraries
License:  MIT
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SZ/SZBALINT/WWW-Curl-%{version}.tar.gz
#Patch0:   WWW-Curl-4.17-curl-7.87.0.patch
Patch0:   WWW-Curl-4.17-curl-8.0.1.patch

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Module::Install)
BuildRequires:  libcurl-devel
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
%endif
# runtime
#Requires:
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif

%description
WWW::Curl is a Perl extension interface for libcurl.

%prep
%setup -n %{cpanname}-%{version}
%patch 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"

%__sed -i '/DEPRECAT/d' curlopt-constants.c
%__sed -i '/STRICTER/d' curlopt-constants.c
%__sed -i '/return CURL_WIN32;/d' curlopt-constants.c
%__sed -i '/return CURLOPT;/d' curlopt-constants.c

make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make test > %{name}-make.test.log 2>&1
%else
echo "make test not run during package build." > %{name}-make.test.log
%endif

%install
make install DESTDIR=%{buildroot}

# if binary
%{_fixperms} %{buildroot}%{perl5_vendorarch}

%if 0%{?perl5_cpanlic:1} == 1
cat > MIT-License.txt << "EOF"
This package specifies it uses the MIT licenses but did not include
the license in the package source.

The MIT license can be found in the following directory:

  %{perl5_cpanlic}/MIT/

EOF
%endif

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorarch}/WWW
%attr(0444,root,root) %{perl5_vendorarch}/WWW/Curl.pm
%dir %{perl5_vendorarch}/WWW/Curl
%attr(0444,root,root) %{perl5_vendorarch}/WWW/Curl/Easy.pm
%attr(0444,root,root) %{perl5_vendorarch}/WWW/Curl/Form.pm
%attr(0444,root,root) %{perl5_vendorarch}/WWW/Curl/Multi.pm
%attr(0444,root,root) %{perl5_vendorarch}/WWW/Curl/Share.pm
%dir %{perl5_vendorarch}/auto/WWW
%dir %{perl5_vendorarch}/auto/WWW/Curl
%attr(0555,root,root) %{perl5_vendorarch}/auto/WWW/Curl/Curl.so
%attr(0644,root,root) %{_mandir}/man3/WWW::Curl.3*
%if 0%{?perl5_cpanlic:1} == 1
%license LICENSE MIT-License.txt
%doc Changes README LICENSE MIT-License.txt
%else
%license LICENSE
%doc Changes README LICENSE
%endif
%doc %{name}-make.test.log



%changelog
* Tue May 09 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.17-0.rc1
- Initial spec file
