# DEV RELEASE --- necessary due to LibreSSL version

%global cpanname Net-SSLeay

Name:     perl-%{cpanname}
Version:  1.93
Release:  %{?repo}0.rc2%{?dist}
Summary:  Perl bindings for OpenSSL and LibreSSL

Group:    Development/Libraries
License:  Artistic-2.0
URL:      https://metacpan.org/dist/%{cpanname}
#Source0:  https://cpan.metacpan.org/authors/id/C/CH/CHRISN/%%{cpanname}-%%{version}.tar.gz
Source0:  https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-1.93_01.tar.gz

BuildRequires:  zlib-devel
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
BuildRequires:  libressl-openssl-compat
%else
BuildRequires:  openssl-devel
BuildRequires:  openssl
%endif
BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(English)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(constant)
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(SelectSaver)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(base)
BuildRequires:  perl(MIME::Base64)
%endif
# runtime
Requires: perl(MIME::Base64)
# /end runtime
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif

%description
This module provides Perl bindings for libssl (an SSL/TLS API) and
libcrypto (a cryptography API).

%prep
#%%setup -n %%{cpanname}-%%{version}
%setup -n %{cpanname}-%{version}_01
# avoid bogus dependencies
%__chmod -c 644 examples/*


%build
PERL_MM_USE_DEFAULT=1 \
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

# if binary
%{_fixperms} %{buildroot}%{perl5_vendorarch}

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorarch}/Net
%attr(0444,root,root) %{perl5_vendorarch}/Net/SSLeay.pm
%dir %{perl5_vendorarch}/Net/SSLeay
%attr(0444,root,root) %{perl5_vendorarch}/Net/SSLeay/Handle.pm
%attr(0444,root,root) %{perl5_vendorarch}/Net/SSLeay.pod
%dir %{perl5_vendorarch}/auto/Net
%dir %{perl5_vendorarch}/auto/Net/SSLeay
%attr(0444,root,root) %{perl5_vendorarch}/auto/Net/SSLeay/*.al
%attr(0444,root,root) %{perl5_vendorarch}/auto/Net/SSLeay/autosplit.ix
%attr(0555,root,root) %{perl5_vendorarch}/auto/Net/SSLeay/SSLeay.so
%attr(0644,root,root) %{_mandir}/man3/Net::SSLeay.3*
%attr(0644,root,root) %{_mandir}/man3/Net::SSLeay::Handle.3*
%license LICENSE
%doc Changes CONTRIBUTING.md Credits LICENSE QuickRef README examples
%doc %{name}-make.test.log



%changelog
* Sun May 21 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.93-0.rc2
- Fix BuildRequires for openssl-compat

* Sat Apr 29 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.93-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
