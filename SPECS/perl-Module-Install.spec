%global cpanname Module-Install

Name:     perl-%{cpanname}
Version:  1.21
Release:  %{?repo}0.rc1%{?dist}
Summary:  Standalone, extensible Perl module installer
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(YAML::Tiny)
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Remove)
BuildRequires:  perl(File::Path)
%endif
# runtime
Requires: perl(File::Remove)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif
%if 0%{?perl5_cpanlic:1} == 1
Requires: common-CPAN-licenses
%endif

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly
correct manner with ExtUtils::MakeMaker, and will run on any Perl
installation version 5.005 or newer.

The intent is to make it as easy as possible for CPAN authors (and
especially for first-time CPAN authors) to have installers that follow
all the best practices for distribution installation, but involve as
much DWIM (Do What I Mean) as possible when writing them.


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

%if 0%{?perl5_cpanlic:1} == 1
cat > Perl5-Licenses.txt << "EOF"
This package specifies it uses the Perl 5 licenses but did not include
them in the package source.

They can be found in the following directory:

  %{perl5_cpanlic}/Perl5/

EOF
%endif

%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Module
%attr(0444,root,root) %{perl5_vendorlib}/Module/AutoInstall.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install.pod
%dir %{perl5_vendorlib}/Module/Install
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/API.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin.pm
%dir %{perl5_vendorlib}/Module/Install/Admin
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Bundle.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Compiler.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Find.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Include.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Makefile.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Manifest.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/Metadata.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/ScanDeps.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Admin/WriteAll.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/AutoInstall.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Base.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Bundle.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Can.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Compiler.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Deprecated.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/External.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/FAQ.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Fetch.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Include.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Inline.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/MakeMaker.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Makefile.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Metadata.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/PAR.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Philosophy.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Run.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Scripts.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Share.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/Win32.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/With.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Install/WriteAll.pm
%dir %{perl5_vendorlib}/inc
%dir %{perl5_vendorlib}/inc/Module
%attr(0444,root,root) %{perl5_vendorlib}/inc/Module/Install.pm
%attr(0644,root,root) %{_mandir}/man3/Module::AutoInstall.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::API.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Admin.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Admin::Include.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Admin::Manifest.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Base.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Bundle.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Can.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Compiler.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Deprecated.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::External.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::FAQ.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Makefile.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::PAR.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Philosophy.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::Share.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Install::With.3*
%attr(0644,root,root) %{_mandir}/man3/inc::Module::Install.3*
%if 0%{?perl5_cpanlic:1} == 1
%license Perl5-Licenses.txt
%doc Changes README TODO Perl5-Licenses.txt
%else
%doc Changes README TODO
%endif
%doc %{name}-make.test.log



%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.21-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
