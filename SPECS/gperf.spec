%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     gperf
Version:  3.1
Release:  %{?repo}0.1%{?dist}
Summary:  perfect hash function generator

Group:    Development/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/gperf/
Source0:  https://ftp.gnu.org/gnu/gperf/gperf-%{version}.tar.gz

BuildRequires:    libstdc++-devel
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
GNU gperf is a perfect hash function generator. For a given list of
strings, it produces a hash function and hash table, in form of C or
C++ code, for looking up a value depending on the input string. The
hash function is *perfect*, which means that the hash table has no
collisions, and the hash table lookup needs a single string comparison
only.

GNU gperf is highly customizable. There are options for generating C
or C++ code, for emitting switch statements or nested ifs instead of a
hash table, and for tuning the algorithm employed by gperf.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
# known to fail if parallec check is done
make -j1 check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/doc/gperf.html

%post
%{insinfo} %{_infodir}/gperf.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gperf.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gperf
%attr(0644,root,root) %{_infodir}/gperf.info*
%attr(0644,root,root) %{_mandir}/man1/gperf.1*
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README doc/*.html



%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
