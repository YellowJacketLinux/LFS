%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     automake
Version:  1.16.5
Release:	%{?repo}0.rc1%{?dist}
Summary:  tool for automatically generating Makefile.in files
BuildArch:  noarch

Group:    Development/Utilities
License:  GPL-2.0-or-later
URL:      https://www.gnu.org/software/automake/
Source0:  https://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz

#BuildRequires:
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}	

%description
GNU Automake is a tool for automatically generating Makefile.in files
compliant with the GNU Coding Standards. Automake requires the use of
GNU Autoconf.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make %{_smp_mflags} check > %{name}-make.check.log 2>&1
%else
echo "make check not run at package build." > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_datadir}/doc/automake/amhello-1.0.tar.gz

%post
%{insinfo} %{_infodir}/automake-history.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/automake.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/automake-history.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/automake.info %{_infodir}/dir ||:
fi

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/aclocal
%attr(0755,root,root) %{_bindir}/aclocal-1.16
%attr(0755,root,root) %{_bindir}/automake
%attr(0755,root,root) %{_bindir}/automake-1.16
%dir %{_datadir}/aclocal
%attr(0644,root,root) %{_datadir}/aclocal/README
%dir %{_datadir}/aclocal-1.16
%attr(0644,root,root) %{_datadir}/aclocal-1.16/*.m4
%dir %{_datadir}/aclocal-1.16/internal
%attr(0644,root,root) %{_datadir}/aclocal-1.16/internal/ac-config-macro-dirs.m4
%dir %{_datadir}/automake-1.16
%dir %{_datadir}/automake-1.16/Automake
%attr(0644,root,root) %{_datadir}/automake-1.16/Automake/*.pm
%attr(0644,root,root) %{_datadir}/automake-1.16/COPYING
%attr(0644,root,root) %{_datadir}/automake-1.16/INSTALL
%dir %{_datadir}/automake-1.16/am
%attr(0644,root,root) %{_datadir}/automake-1.16/am/*.am
%attr(0755,root,root) %{_datadir}/automake-1.16/ar-lib
%attr(0755,root,root) %{_datadir}/automake-1.16/compile
%attr(0755,root,root) %{_datadir}/automake-1.16/config.guess
%attr(0755,root,root) %{_datadir}/automake-1.16/config.sub
%attr(0755,root,root) %{_datadir}/automake-1.16/depcomp
%attr(0755,root,root) %{_datadir}/automake-1.16/install-sh
%attr(0755,root,root) %{_datadir}/automake-1.16/mdate-sh
%attr(0755,root,root) %{_datadir}/automake-1.16/missing
%attr(0755,root,root) %{_datadir}/automake-1.16/mkinstalldirs
%attr(0755,root,root) %{_datadir}/automake-1.16/py-compile
%attr(0755,root,root) %{_datadir}/automake-1.16/tap-driver.sh
%attr(0755,root,root) %{_datadir}/automake-1.16/test-driver
%attr(0644,root,root) %{_datadir}/automake-1.16/texinfo.tex
%attr(0755,root,root) %{_datadir}/automake-1.16/ylwrap
%attr(0644,root,root) %{_infodir}/automake-history.info*
%attr(0644,root,root) %{_infodir}/automake.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/aclocal-1.16.1*
%attr(0644,root,root) %{_mandir}/man1/aclocal.1*
%attr(0644,root,root) %{_mandir}/man1/automake-1.16.1*
%attr(0644,root,root) %{_mandir}/man1/automake.1*
%license COPYING
%doc AUTHORS ChangeLog COPYING HACKING NEWS NEWS-2.0 README THANKS
%doc doc/amhello-1.0.tar.gz
%doc %{name}-make.check.log



%changelog
* Sun May 07 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.44-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
