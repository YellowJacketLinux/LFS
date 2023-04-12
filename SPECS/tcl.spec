Name:     tcl
Version:  8.6.13
Release:  %{?repo}0.rc2%{?dist}
Summary:  Tool Command Language

Group:    Programming/Languages
License:  TCL
URL:      https://www.tcl-lang.org/
Source0:  https://downloads.sourceforge.net/tcl/tcl%{version}-src.tar.gz
Source1:  https://downloads.sourceforge.net/tcl/tcl%{version}-html.tar.gz

BuildRequires:  zlib-devel
#Requires:	

%description
Tcl (Tool Command Language) is a very powerful but easy to learn dynamic
programming language, suitable for a very wide range of uses, including
web and desktop applications, networking, administration, testing and
many more.

%package devel
Summary:  Developer files for tcl
Group:    Development/Languages
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer header files needed to compile
software that links against the tcl library, as well as the developer
man page documentation.

%prep
%setup -n %{name}%{version}


%build
SRCDIR=$(pwd)
cd unix
%configure
make %{?_smp_mflags}
sed -e "s|$SRCDIR/unix|%{_libdir}|" \
    -e "s|$SRCDIR|%{_includedir}|"  \
    -i tclConfig.sh

sed -e "s|$SRCDIR/unix/pkgs/tdbc1.1.5|%{_libdir}/tdbc1.1.5|" \
    -e "s|$SRCDIR/pkgs/tdbc1.1.5/generic|%{_includedir}|"    \
    -e "s|$SRCDIR/pkgs/tdbc1.1.5/library|%{_libdir}/tcl8.6|" \
    -e "s|$SRCDIR/pkgs/tdbc1.1.5|%{_includedir}|"            \
    -i pkgs/tdbc1.1.5/tdbcConfig.sh

sed -e "s|$SRCDIR/unix/pkgs/itcl4.2.3|%{_libdir}/itcl4.2.3|" \
    -e "s|$SRCDIR/pkgs/itcl4.2.3/generic|%{_includedir}|"    \
    -e "s|$SRCDIR/pkgs/itcl4.2.3|%{_includedir}|"            \
    -i pkgs/itcl4.2.3/itclConfig.sh

unset SRCDIR

%check
cd unix
make test > ../%{name}-make.test.log 2>&1

%install
cd unix
make install DESTDIR=%{buildroot}
chmod -v u+w %{buildroot}%{_libdir}/libtcl8.6.so

make install-private-headers DESTDIR=%{buildroot}

ln -sf tclsh8.6 %{buildroot}%{_bindir}/tclsh

mv %{buildroot}%{_mandir}/man3/Thread.3 %{buildroot}%{_mandir}/man3/Tcl_Thread.3
cd ..
tar -xf %{SOURCE1} --strip-components=1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libtcl8.6.so
%attr(0755,root,root) %{_bindir}/sqlite3_analyzer
%attr(0755,root,root) %{_bindir}/tclsh8.6
%{_bindir}/tclsh
# these likely belong in subpackages
# directories and contents - perhaps should
#  be in %%{_prefix}/lib ???
%attr(0755,root,root) %dir %{_libdir}/itcl4.2.3
%attr(0644,root,root) %{_libdir}/itcl4.2.3/*.a
%attr(0644,root,root) %{_libdir}/itcl4.2.3/*.sh
%attr(0644,root,root) %{_libdir}/itcl4.2.3/*.so
%attr(0644,root,root) %{_libdir}/itcl4.2.3/*.tcl
%attr(0755,root,root) %dir %{_libdir}/sqlite3.40.0
%attr(0644,root,root) %{_libdir}/sqlite3.40.0/*.so
%attr(0644,root,root) %{_libdir}/sqlite3.40.0/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tcl8
%attr(0755,root,root) %dir %{_libdir}/tcl8/8.4
%attr(0644,root,root) %{_libdir}/tcl8/8.4/platform-1.0.19.tm
%attr(0755,root,root) %dir %{_libdir}/tcl8/8.4/platform
%attr(0644,root,root) %{_libdir}/tcl8/8.4/platform/shell-1.1.4.tm
%attr(0755,root,root) %dir %{_libdir}/tcl8/8.5
%attr(0644,root,root) %{_libdir}/tcl8/8.5/*.tm
%attr(0755,root,root) %dir %{_libdir}/tcl8/8.6
%attr(0644,root,root) %{_libdir}/tcl8/8.6/http-2.9.8.tm
%attr(0755,root,root) %dir %{_libdir}/tcl8/8.6/tdbc
%attr(0644,root,root) %{_libdir}/tcl8/8.6/tdbc/sqlite3-1.1.5.tm
%attr(0755,root,root) %dir %{_libdir}/tcl8.6
%attr(0644,root,root) %{_libdir}/tcl8.6/*.tcl
%attr(0644,root,root) %{_libdir}/tcl8.6/tclAppInit.c
%attr(0644,root,root) %{_libdir}/tcl8.6/tclIndex
%attr(0755,root,root) %dir %{_libdir}/tcl8.6/encoding
%attr(0644,root,root) %{_libdir}/tcl8.6/encoding/*.enc
%attr(0755,root,root) %dir %{_libdir}/tcl8.6/http1.0
%attr(0644,root,root) %{_libdir}/tcl8.6/http1.0/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tcl8.6/msgs
%attr(0644,root,root) %{_libdir}/tcl8.6/msgs/*.msg
%attr(0755,root,root) %dir %{_libdir}/tcl8.6/opt0.4
%attr(0644,root,root) %{_libdir}/tcl8.6/opt0.4/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tdbc1.1.5
%attr(0644,root,root) %{_libdir}/tdbc1.1.5/*.a
%attr(0644,root,root) %{_libdir}/tdbc1.1.5/*.sh
%attr(0644,root,root) %{_libdir}/tdbc1.1.5/*.so
%attr(0644,root,root) %{_libdir}/tdbc1.1.5/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tdbcmysql1.1.5
%attr(0644,root,root) %{_libdir}/tdbcmysql1.1.5/libtdbcmysql1.1.5.so
%attr(0644,root,root) %{_libdir}/tdbcmysql1.1.5/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tdbcodbc1.1.5
%attr(0644,root,root) %{_libdir}/tdbcodbc1.1.5/libtdbcodbc1.1.5.so
%attr(0644,root,root) %{_libdir}/tdbcodbc1.1.5/*.tcl
%attr(0755,root,root) %dir %{_libdir}/tdbcpostgres1.1.5
%attr(0644,root,root) %{_libdir}/tdbcpostgres1.1.5/libtdbcpostgres1.1.5.so
%attr(0644,root,root) %{_libdir}/tdbcpostgres1.1.5/*.tcl
%attr(0755,root,root) %dir %{_libdir}/thread2.8.8
%attr(0644,root,root) %{_libdir}/thread2.8.8/libthread2.8.8.so
%attr(0644,root,root) %{_libdir}/thread2.8.8/*.tcl
%attr(0644,root,root) %{_mandir}/man1/tclsh.1*
%attr(0644,root,root) %{_mandir}/mann/*.n*
%license license.terms
%doc changes license.terms html
%doc %{name}-make.test.log

%files devel
%defattr(-,root,root,-)
# this probably should be 0644
%attr(0755,root,root) %{_libdir}/libtclstub8.6.a
%attr(0644,root,root) %{_libdir}/tclConfig.sh
%attr(0644,root,root) %{_libdir}/tclooConfig.sh
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_libdir}/pkgconfig/tcl.pc
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license license.terms


%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 8.6.13-0.rc2
- Rebuild with newly packaged gcc

* Mon Mar 27 2023 Michael A. Peters <anymouseprophet@gmail.com> - 8.6.13-0.rc1
- Initial spec file for YJL, libraries probably need to be split off
- into a -libs package
