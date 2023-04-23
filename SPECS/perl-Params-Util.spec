%global cpanname Params-Util

%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global norequireautoconf foo
%global norequireleaktrace bar
%endif
%endif

Name:     perl-%{cpanname}
Version:  1.102
Release:  %{?repo}0.rc3%{?dist}
Summary:  Simple, compact and correct param-checking functions

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/pod/Params::Util
Source0:  https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Params-Util-1.102.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(parent)
%if 0%{!?norequireautoconf:1}
BuildRequires:  perl(Config::AutoConf) >= 0.315
%endif
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(warnings)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Scalar::Util) >= 1.18
BuildRequires:  perl(XSLoader) >= 0.22
%if 0%{!?norequireleaktrace:1}
BuildRequires:  perl(Test::LeakTrace)
%endif
%endif
# Runtime
Requires: perl(Scalar::Util) >= 1.18
Requires: perl(XSLoader) >= 0.22
%if 0%{?perl5_ABI:1} == 1
Requires: %{perl5_ABI}
%endif

%description
Params::Util provides a basic set of importable functions that makes
checking parameters a hell of a lot easier.

While they can be (and are) used in other contexts, the main point
behind this module is that the functions both Do What You Mean, and Do
The Right Thing, so they are most useful when you are getting params
passed into your code from someone and/or somewhere else and you can't
really trust the quality.

Thus, Params::Util is of most use at the edges of your API, where
params and data are coming in from outside your code.

%prep
%setup -n %{cpanname}-%{version}
chmod -x Changes


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
%{_fixperms} %{buildroot}%{perl5_vendorarch}


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorarch}/Params
%attr(0444,root,root) %{perl5_vendorarch}/Params/Util.pm
%dir %{perl5_vendorarch}/Params/Util
%attr(0444,root,root) %{perl5_vendorarch}/Params/Util/PP.pm
%dir %{perl5_vendorarch}/auto/Params
%dir %{perl5_vendorarch}/auto/Params/Util
%attr(0555,root,root) %{perl5_vendorarch}/auto/Params/Util/Util.so
%attr(0644,root,root) %{_mandir}/man3/Params::Util.3*
%attr(0644,root,root) %{_mandir}/man3/Params::Util::PP.3*
%license ARTISTIC-1.0 GPL-1 LICENSE
%doc ARTISTIC-1.0 GPL-1 LICENSE Changes README.md
%doc %{name}-make.test.log



%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.102-0.rc3
- BuildRequires perl-devel
- Conditionally BuildRequire Config::AutoConf and Test::LeakTrace
- Conditionally run tests
- Require %%perl5_ABI

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.102-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
