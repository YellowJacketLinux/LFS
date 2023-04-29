%global cpanname Business-ISBN-Data

Name:     perl-%{cpanname}
Version:  20230426.001
Release:  %{?repo}0.rc1%{?dist}
Summary:  Data pack for Business-ISBN
BuildArch:  noarch

Group:    Development/Libraries
License:  Artistic-2.0
URL:      https://metacpan.org/pod/Business::ISBN::Data
Source0:  https://cpan.metacpan.org/authors/id/B/BD/BDFOY/Business-ISBN-Data-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec::Functions)
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
%endif
# runtime
Requires: perl(Carp)
Requires: perl(File::Basename)
Requires: perl(File::Spec::Functions)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Business::ISBN::Data - data pack for Business::ISBN

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

# if binary
#%{_fixperms} %{buildroot}%{perl5_vendorarch}


%files
%defattr(-,root,root,-)
%license LICENSE
%dir %{perl5_vendorlib}/Business
%dir %{perl5_vendorlib}/Business/ISBN
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN/Data.pm
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN/RangeMessage.url
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN/RangeMessage.xml
%attr(0644,root,root) %{_mandir}/man3/Business::ISBN::Data.3*
%doc Changes LICENSE examples
%doc %{name}-make.test.log



%changelog
* Fri Apr 28 Michael A. Peters <anymouseprophet@gmail.com> - 20230426.001-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
