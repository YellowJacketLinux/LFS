%global cpanname Capture-Tiny

Name:     perl-%{cpanname}
Version:  0.48
Release:  %{?repo}0.rc1%{?dist}
Summary:  Capture STDOUT and STDERR from Perl, XS or external programs

Group:    Development/Libraries
License:  Apache 2.0
URL:      https://metacpan.org/pod/Capture::Tiny
Source0:  https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/%{cpanname}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
# for test
BuildRequires:  perl(Test::More) perl(warnings)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(CPAN::Meta)

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
make test > %{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}%{perl5_vendorlib}


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/Capture
%attr(0444,root,root) %{perl5_vendorlib}/Capture/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/Capture::Tiny.3*
%doc %{name}-make.test.log
%doc examples README



%changelog
* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.48-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
