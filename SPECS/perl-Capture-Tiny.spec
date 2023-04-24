%global cpanname Capture-Tiny

Name:     perl-%{cpanname}
Version:  0.48
Release:  %{?repo}0.rc3%{?dist}
Summary:  Capture STDOUT and STDERR from Perl, XS or external programs

Group:    Development/Libraries
License:  Apache-2.0
URL:      https://metacpan.org/pod/Capture::Tiny
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:	perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(IO::File)
BuildRequires:  perl(CPAN::Meta) >= 2.120900
BuildRequires:  perl(lib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
%endif
# runtime
Requires: perl(Carp)
Requires: perl(Exporter)
Requires: perl(File::Spec)
Requires: perl(File::Temp)
Requires: perl(IO::Handle)
Requires: perl(Scalar::Util)
Requires: perl(strict)
Requires: perl(warnings)
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
Capture::Tiny provides a simple, portable way to capture almost anything
sent to STDOUT or STDERR, regardless of whether it comes from Perl, from
XS code or from an external program. Optionally, output can be teed so
that it is captured while being passed through to the original file-
handles.

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
%dir %{perl5_vendorlib}/Capture
%attr(0444,root,root) %{perl5_vendorlib}/Capture/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Capture::Tiny.3*
%license LICENSE
%doc Changes LICENSE README Todo examples
%doc %{name}-make.test.log


%changelog
* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.48-0.rc3
- BuildRequire perl-devel

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.48-0.rc2
- Add %%license, run tests conditionally, require %%perl5_API

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.48-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
