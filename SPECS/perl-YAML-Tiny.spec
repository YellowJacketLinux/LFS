%global cpanname YAML-Tiny

Name:     perl-%{cpanname}
Version:  1.74
Release:  %{?repo}0.rc1%{?dist}
Summary:  Read/Write YAML files with as little code as possible
BuildArch:  noarch

Group:    Development/Libraries
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://metacpan.org/dist/%{cpanname}
Source0:  https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz

BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# for test
%if 0%{?runtests:1} == 1
BuildRequires:  perl(Test::More)
%endif
# runtime
#Requires:
# /end runtime
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description
The YAML specification is huge. Really, really huge. It contains all
the functionality of XML, except with flexibility and choice, which
makes it easier to read, but with a formal specification that is more
complex than XML.

Like the other ::Tiny modules, YAML::Tiny has no non-core dependencies,
does not require a compiler to install, is back-compatible to Perl v5.8.1,
and can be inlined into other modules if needed.

In exchange for adding this extreme flexibility, it provides support
for only a limited subset of YAML. But the subset supported contains
most of the features for the more common uses of YAML.

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
%dir %{perl5_vendorlib}/YAML
%attr(0444,root,root) %{perl5_vendorlib}/YAML/Tiny.pm
%attr(0644,root,root) %{_mandir}/man3/YAML::Tiny.3*
%license LICENSE
%doc Changes LICENSE README
%doc %{name}-make.test.log



%changelog
* Mon May 08 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.74-0.rc1
- Initial spec file
