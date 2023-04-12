# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     flex
Version:  2.6.4
Release:  %{?repo}0.rc2%{?dist}
Summary:  Fast Lexical Analizer

Group:    Programming/Utilities
License:  BSD Style
URL:      https://github.com/westes/flex
Source0:  https://github.com/westes/flex/releases/download/v%{version}/flex-%{version}.tar.gz

#BuildRequires:	
Requires: libfl = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
This is flex, the fast lexical analyzer generator.

flex is a tool for generating scanners: programs which recognize lexical
patterns in text.

%package -n libfl
Summary:  The flex libfl shared library
Group:    System Environment/Libraries

%description -n libfl
This package contains the libfl shared library.

%package -n libfl-devel
Summary:  Developer file
Group:    Development/Libraries
Requires: libfl = %{version}-%{release}

%description -n libfl-devel
This package contains the developer files needed to compile software
that links against libfl.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%check
make check > flex-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
ln -s flex %{buildroot}%{_bindir}/lex
rm -rf %{buildroot}%{_datadir}/doc/flex
%find_lang %{name}

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%post -n libfl -p /sbin/ldconfig
%postun -n libfl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/flex
%{_bindir}/flex++
%{_bindir}/lex
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/flex.info*
%attr(0644,root,root) %{_mandir}/man1/flex.1*
%license COPYING
%doc AUTHORS COPYING NEWS ONEWS README.md THANKS ChangeLog
%doc flex-make.check.log

%files -n libfl
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libfl.so.2.0.0
%{_libdir}/libfl.so.2
%license COPYING

%files -n libfl-devel
%defattr(-,root,root,-)
%{_libdir}/libfl.so
%attr(0644,root,root) %{_includedir}/FlexLexer.h
%license COPYING

%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.6.4-0.rc2
- Rebuild with newly packaged gcc

* Sat Mar 25 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.6.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
