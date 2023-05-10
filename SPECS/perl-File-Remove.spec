%global cpanname File-Remove

Name:     perl-%{cpanname}
Version:  1.61
Release:  %{?repo}0.rc1%{?dist}
Summary:  Remove files and directories
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/%{cpanname}-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(Module::Build) >= 0.28
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec) >= 3.29
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Cwd) >= 3.29
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
%endif
# runtime
Requires: perl(Cwd) >= 3.29
Requires: perl(File::Glob)
Requires: perl(File::Path)
Requires: perl(File::Spec) >= 3.29
Requires: perl(constant)
Requires: perl(strict)
Requires: perl(vars)
Requires: perl(warnings)
# /end runtime
# Change both perl5_API below to perl5_ABI for binary packages
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
File::Remove::remove removes files and directories. It acts like /bin/rm,
for the most part. Although unlink can be given a list of files, it
will not remove directories; this module remedies that. It also accepts
wildcards, * and ?, as arguments for filenames.

File::Remove::trash accepts the same arguments as remove, with the
addition of an optional, infrequently used "other platforms" hashref.

%prep
%setup -n %{cpanname}-%{version}


%build
perl Build.PL destdir=%{buildroot} installdirs=vendor
./Build


%check
%if 0%{?runtests:1} == 1
./Build test > %{name}-Build.test.log 2>&1
%else
echo "make test not run during package build." > %{name}-Build.test.log
%endif

%install
./Build install DESTDIR=%{buildroot}
rm -f %{buildroot}%{perl5_vendorarch}/auto/File/Remove/.packlist


%files
%defattr(-,root,root,-)
%dir %{perl5_vendorarch}/File
%attr(0444,root,root) %{perl5_vendorarch}/File/Remove.pm
%attr(0644,root,root) %{_mandir}/man3/File::Remove.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-Build.test.log



%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.61-0.rc1
- Initial spec file for YJL
