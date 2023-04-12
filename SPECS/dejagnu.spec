# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     dejagnu
Version:  1.6.3
Release:  %{?repo}0.rc2%{?dist}
Summary:  Framework for testing other programs

Group:    Development/Testing
License:  GPLv3
URL:      https://www.gnu.org/software/dejagnu/
Source0:  https://ftp.gnu.org/gnu/dejagnu/%{name}-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:  expect-devel
BuildRequires:  tcl-devel
Requires: expect
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
DejaGnu is a framework for testing other programs. Its purpose is to
provide a single front end for all tests. Think of it as a custom library
of Tcl procedures crafted to support writing a test harness. A test
harness is the testing infrastructure that is created to support a
specific program or tool. Each program can have multiple testsuites,
all supported by a single test harness. DejaGnu is written in Expect,
which in turn uses Tcl -- Tool command language.

%package devel
Group:    Development/Libraries
Summary:  Dejagnu header file
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the dejagnu header file.


%prep
%setup -q


%build
mkdir build && cd build
../configure --prefix=%{_prefix}
makeinfo --html --no-split -o doc/dejagnu.html ../doc/dejagnu.texi
makeinfo --plaintext       -o doc/dejagnu.txt  ../doc/dejagnu.texi
#make %%{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot}


%check
cd build
make check > %{name}-make.check.log 2>&1


%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/dejagnu
%attr(0755,root,root) %{_bindir}/runtest
%{_datadir}/%{name}
%attr(0644,root,root) %{_infodir}/%{name}.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/*.1*
%license COPYING
%doc build/%{name}-make.check.log build/doc/dejagnu.html build/doc/dejagnu.txt
%doc AUTHORS ChangeLog* COPYING MAINTAINERS NEWS README TODO

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/dejagnu.h


%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.6.3-0.rc2
- Use %%{insinfo} macro.

* Tue Apr 04 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.6.3-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
