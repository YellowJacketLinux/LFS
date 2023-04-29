%global cpanname Business-ISBN

Name:     perl-%{cpanname}
Version:  3.008
Release:  %{?repo}0.rc1%{?dist}
Summary:  work with International Standard Book Numbers
BuildArch:  noarch

Group:    Development/Libraries
License:  Artistic-2.0
URL:      https://metacpan.org/dist/Business-ISBN
Source0:  https://cpan.metacpan.org/authors/id/B/BD/BDFOY/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec::Functions)
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Business::ISBN::Data) >= 20230322.001
%endif
# runtime
Requires: perl(Business::ISBN::Data) >= 20230322.001
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This modules handles International Standard Book Numbers, including
ISBN-10 and ISBN-13.

The data come from Business::ISBN::Data, which means you can update the
data separately from the code. Also, you can use Business::ISBN::Data
with whatever RangeMessage.xml you like if you have updated data. See
that module for details.

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
%dir %{perl5_vendorlib}/Business
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN.pm
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN10.pm
%attr(0444,root,root) %{perl5_vendorlib}/Business/ISBN13.pm
%attr(0644,root,root) %{_mandir}/man3/Business::ISBN.3*
%attr(0644,root,root) %{_mandir}/man3/Business::ISBN10.3*
%attr(0644,root,root) %{_mandir}/man3/Business::ISBN13.3*
%license LICENSE
%doc Changes LICENSE examples
%doc %{name}-make.test.log



%changelog
* Fri Apr 28 Michael A. Peters <anymouseprophet@gmail.com> - 3.008-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
