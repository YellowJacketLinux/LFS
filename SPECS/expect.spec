# FIXME - some examples have unmet dependencies

Name:     expect
Version:  5.45.4
Release:  %{?repo}0.rc2%{?dist}
Summary:  Tool for automating interactive applications

Group:    Programming/Languages
License:  Public Domain
URL:      https://core.tcl-lang.org/expect/index
Source0:  https://prdownloads.sourceforge.net/expect/expect%{version}.tar.gz

BuildRequires:  tcl-devel
Requires:	libexpect = %{version}-%{release}

%description
Expect is a tool for automating interactive applications such as telnet,
ftp, passwd, fsck, rlogin, tip, etc. Expect really makes this stuff
trivial. Expect is also useful for testing these same applications.

%package -n libexpect
Summary:  The libexpect shared library
Group:    System Environment/Libraries

%description -n libexpect
This package contains the libexpect shared library.

%package devel
Summary:  Developer files for expect
Group:    Development/Libraries
Requires: libexpect = %{version}-%{release}

%description devel
This package contains the header files needed to build software that
links against the libexpect library.

%package examples
Summary:  Example programs written in expect
Group:    Misc
Requires: %{name} = %{version}-%{release}
Requires: libexpect = %{version}-%{release}

%description examples
This package contains various example programs that are written in
expect.

%prep
%setup -n %{name}%{version}

%build
%configure \
  --with-tcl=%{_libdir} \
  --enable-shared       \
  --with-tclincludedir=%{_includedir}
make %{?_smp_mflags}

%check
make test > %{name}-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}
ln -sf expect%{version}/libexpect%{version}.so %{buildroot}%{_libdir}

%post -n libexpect -p /sbin/ldconfig
%postun -n libexpect -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/expect
%attr(0644,root,root) %{_mandir}/man1/expect.1*
%license license.terms
%doc %{name}-make.test.log
%doc ChangeLog HISTORY NEWS README license.terms

%files -n libexpect
%defattr(-,root,root,-)
%attr(0755,root,root) %dir %{_libdir}/%{name}%{version}
%attr(0755,root,root) %{_libdir}/%{name}%{version}/libexpect5.45.4.so
%attr(0644,root,root) %{_libdir}/%{name}%{version}/pkgIndex.tcl
%{_libdir}/libexpect5.45.4.so
%license license.terms

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_mandir}/man3/libexpect.3*
%license license.terms

%files examples
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/autoexpect
%attr(0755,root,root) %{_bindir}/autopasswd
%attr(0755,root,root) %{_bindir}/cryptdir
%attr(0755,root,root) %{_bindir}/decryptdir
%attr(0755,root,root) %{_bindir}/dislocate
%attr(0755,root,root) %{_bindir}/ftp-rfc
%attr(0755,root,root) %{_bindir}/kibitz
%attr(0755,root,root) %{_bindir}/lpunlock
%attr(0755,root,root) %{_bindir}/mkpasswd
%attr(0755,root,root) %{_bindir}/multixterm
%attr(0755,root,root) %{_bindir}/passmass
%attr(0755,root,root) %{_bindir}/rftp
%attr(0755,root,root) %{_bindir}/rlogin-cwd
%attr(0755,root,root) %{_bindir}/timed-read
%attr(0755,root,root) %{_bindir}/timed-run
%attr(0755,root,root) %{_bindir}/tknewsbiff
%attr(0755,root,root) %{_bindir}/tkpasswd
%attr(0755,root,root) %{_bindir}/unbuffer
%attr(0755,root,root) %{_bindir}/weather
%attr(0755,root,root) %{_bindir}/xkibitz
%attr(0755,root,root) %{_bindir}/xpstat
%attr(0644,root,root) %{_mandir}/man1/autoexpect.1*
%attr(0644,root,root) %{_mandir}/man1/cryptdir.1*
%attr(0644,root,root) %{_mandir}/man1/decryptdir.1*
%attr(0644,root,root) %{_mandir}/man1/dislocate.1*
%attr(0644,root,root) %{_mandir}/man1/kibitz.1*
%attr(0644,root,root) %{_mandir}/man1/mkpasswd.1*
%attr(0644,root,root) %{_mandir}/man1/multixterm.1*
%attr(0644,root,root) %{_mandir}/man1/passmass.1*
%attr(0644,root,root) %{_mandir}/man1/tknewsbiff.1*
%attr(0644,root,root) %{_mandir}/man1/unbuffer.1*
%attr(0644,root,root) %{_mandir}/man1/xkibitz.1*
%license license.terms
%doc license.terms example/README

%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.45.4-0.rc2
- Rebuild with newly packaged gcc

* Mon Apr 03 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.45.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
