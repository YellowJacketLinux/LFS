%global cpanname IO-Socket-SSL

Name:     perl-%{cpanname}
Version:  2.081
Release:  %{?repo}0.rc2%{?dist}
Summary:  SSL sockets with IO::Socket interface
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SU/SULLR/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(Net::SSLeay) >= 1.59
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Mozilla::CA)
BuildRequires:  perl(Scalar::Util)
%endif
# runtime
Requires: perl(Mozilla::CA)
Requires: perl(Net::SSLeay) >= 1.59
Requires: perl(Scalar::Util)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif

%description
IO::Socket::SSL makes using SSL/TLS much easier by wrapping the necessary
functionality into the familiar IO::Socket interface and providing secure
defaults whenever possible. This way, existing applications can be made
SSL-aware without much effort, at least if you do blocking I/O and don't
use select or poll.

But, under the hood, SSL is a complex beast. So there are lots of methods
to make it do what you need if the default behavior is not adequate.
Because it is easy to inadvertently introduce critical security bugs
or just hard to debug problems, it is recommended you study the
documentation carefully.

%prep
%setup -n %{cpanname}-%{version}


%build
PERL_MM_USE_DEFAULT=1 \
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make test > %{name}-make.test.log 2>&1 ||:
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


# if binary
#%{_fixperms} %{buildroot}%{perl5_vendorarch}

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/IO
%dir %{perl5_vendorlib}/IO/Socket
%attr(0444,root,root) %{perl5_vendorlib}/IO/Socket/SSL.pm
%attr(0444,root,root) %{perl5_vendorlib}/IO/Socket/SSL.pod
%dir %{perl5_vendorlib}/IO/Socket/SSL
%attr(0444,root,root) %{perl5_vendorlib}/IO/Socket/SSL/Intercept.pm
%attr(0444,root,root) %{perl5_vendorlib}/IO/Socket/SSL/PublicSuffix.pm
%attr(0444,root,root) %{perl5_vendorlib}/IO/Socket/SSL/Utils.pm
%attr(0644,root,root) %{_mandir}/man3/IO::Socket::SSL.3*
%attr(0644,root,root) %{_mandir}/man3/IO::Socket::SSL::Intercept.3*
%attr(0644,root,root) %{_mandir}/man3/IO::Socket::SSL::PublicSuffix.3*
%attr(0644,root,root) %{_mandir}/man3/IO::Socket::SSL::Utils.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt
%doc Changes README Perl5-Licenses.txt
%else
%doc Changes README
%endif
%doc %{name}-make.test.log docs example



%changelog
* Sat May 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.081-0.rc2
- Require Mozilla::CA --- while technically not strictly required,
- it allows perl scripts that use TLS to know a cert bundle is available.

* Fri May 05 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.081-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
