%global cpanname Module-Build

Name:     perl-%{cpanname}
Version:  0.4234
Release:  %{?repo}0.rc1%{?dist}
Summary:  Build and install Perl modules
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/L/LE/LEONT/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(CPAN::Meta) >= 2.142060
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(Module::Metadata) >= 1.000002
BuildRequires:  perl(Perl::OSType) >= 1
BuildRequires:  perl(version) >= 0.87
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.003
BuildRequires:  perl(File::Temp) >= 0.15
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4401
BuildRequires:  perl(TAP::Harness) >= 3.29
BuildRequires:  perl(Test::More) >= 0.49
#
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:  perl(ExtUtils::Install) >= 0.3
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(ExtUtils::Mkbootstrap)
BuildRequires:  perl(ExtUtils::ParseXS) >= 2.21
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Text::Abbrev)
BuildRequires:  perl(Text::ParseWords)
%endif
# runtime
Requires: perl(CPAN::Meta) >= 2.142060
Requires: perl(Cwd)
Requires: perl(Data::Dumper)
Requires: perl(ExtUtils::CBuilder) >= 0.27
Requires: perl(ExtUtils::Install) >= 0.3
Requires: perl(ExtUtils::Manifest) >= 1.54
Requires: perl(ExtUtils::Mkbootstrap)
Requires: perl(ExtUtils::ParseXS) >= 2.21
Requires: perl(File::Basename)
Requires: perl(File::Compare)
Requires: perl(File::Copy)
Requires: perl(File::Find)
Requires: perl(File::Path)
Requires: perl(File::Spec) >= 0.82
Requires: perl(Getopt::Long)
Requires: perl(Module::Metadata) >= 1.000002
Requires: perl(Perl::OSType) >= 1
Requires: perl(TAP::Harness) >= 3.29
Requires: perl(Text::Abbrev)
Requires: perl(Text::ParseWords)
Requires: perl(version) >= 0.87
# /end runtime
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
This package is needed to install perl modules that use the Build.PL
build system.

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
rm -f %{buildroot}%{perl5_vendorarch}/auto/Module/Build/.packlist

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/config_data
%dir %{perl5_vendorlib}/Module
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build.pm
%dir %{perl5_vendorlib}/Module/Build
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/API.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Authoring.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Base.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Bundling.pod
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Compat.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Config.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/ConfigData.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Cookbook.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Dumper.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Notes.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/PPMMaker.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/PodParser.pm
%dir %{perl5_vendorlib}/Module/Build/Platform
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/Default.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/MacOS.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/Unix.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/VMS.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/VOS.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/Windows.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/aix.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/cygwin.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/darwin.pm
%attr(0444,root,root) %{perl5_vendorlib}/Module/Build/Platform/os2.pm
%attr(0644,root,root) %{_mandir}/man1/config_data.1*
%attr(0644,root,root) %{_mandir}/man3/Module::Build.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::API.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Authoring.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Base.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Bundling.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::ConfigData.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Compat.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Cookbook.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Notes.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::PPMMaker.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::Default.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::MacOS.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::Unix.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::VMS.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::VOS.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::Windows.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::aix.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::cygwin.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::darwin.3*
%attr(0644,root,root) %{_mandir}/man3/Module::Build::Platform::os2.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.4234-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
