%if 0%{!?__sed:1} == 1
%global __sed %{_bindir}/sed
%endif
%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     autoconf
Version:  2.71
Release:  %{?repo}0.rc1%{?dist}
Summary:  extensible package of M4 macros
BuildArch:  noarch

Group:    Development/Utilities
License:  GPL-3.0-or-later with Exception
URL:      https://www.gnu.org/software/autoconf/
Source0:  https://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz

BuildRequires:    m4 >= 1.4.13
BuildRequires:    %{__sed}
Requires:         m4 >= 1.4.13
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
Autoconf is an extensible package of M4 macros that produce shell scripts
to automatically configure software source code packages. These scripts
can adapt the packages to many kinds of UNIX-like systems without manual
user intervention. Autoconf creates a configuration script for a package
from a template file that lists the operating system features that the
package can use, in the form of M4 macro calls.


%prep
%setup -q
# fix several problems with the tests caused by bash-5.2 and later
%{__sed} -e 's/SECONDS|/&SHLVL|/'        \
  -e '/BASH_ARGV=/a\        /^SHLVL=/ d' \
  -i.orig tests/local.at


%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
export TESTSUITEFLAGS=%{?_smp_mflags}
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run at package build." > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}

%post
%{insinfo} %{_infodir}/autoconf.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/standards.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/autoconf.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/standards.info %{_infodir}/dir ||:
fi


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/autoconf
%attr(0755,root,root) %{_bindir}/autoheader
%attr(0755,root,root) %{_bindir}/autom4te
%attr(0755,root,root) %{_bindir}/autoreconf
%attr(0755,root,root) %{_bindir}/autoscan
%attr(0755,root,root) %{_bindir}/autoupdate
%attr(0755,root,root) %{_bindir}/ifnames
%dir %{_datadir}/autoconf
%dir %{_datadir}/autoconf/Autom4te
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/C4che.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/ChannelDefs.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/Channels.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/Config.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/Configure_ac.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/FileUtils.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/General.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/Getopt.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/Request.pm
%attr(0644,root,root) %{_datadir}/autoconf/Autom4te/XFile.pm
%attr(0644,root,root) %{_datadir}/autoconf/INSTALL
%dir %{_datadir}/autoconf/autoconf
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autoconf.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autoconf.m4f
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autoheader.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autoscan.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autotest.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/autoupdate.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/c.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/erlang.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/fortran.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/functions.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/general.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/go.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/headers.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/lang.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/libs.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/oldnames.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/programs.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/specific.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/status.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/trailer.m4
%attr(0644,root,root) %{_datadir}/autoconf/autoconf/types.m4
%attr(0644,root,root) %{_datadir}/autoconf/autom4te.cfg
%dir %{_datadir}/autoconf/autoscan
%attr(0644,root,root) %{_datadir}/autoconf/autoscan/autoscan.list
%dir %{_datadir}/autoconf/autotest
%attr(0644,root,root) %{_datadir}/autoconf/autotest/autotest.m4
%attr(0644,root,root) %{_datadir}/autoconf/autotest/autotest.m4f
%attr(0644,root,root) %{_datadir}/autoconf/autotest/general.m4
%attr(0644,root,root) %{_datadir}/autoconf/autotest/specific.m4
%dir %{_datadir}/autoconf/build-aux
%attr(0755,root,root) %{_datadir}/autoconf/build-aux/config.guess
%attr(0755,root,root) %{_datadir}/autoconf/build-aux/config.sub
%attr(0755,root,root) %{_datadir}/autoconf/build-aux/install-sh
%dir %{_datadir}/autoconf/m4sugar
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/foreach.m4
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/m4sh.m4
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/m4sh.m4f
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/m4sugar.m4
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/m4sugar.m4f
%attr(0644,root,root) %{_datadir}/autoconf/m4sugar/version.m4
%attr(0644,root,root) %{_infodir}/autoconf.info*
%attr(0644,root,root) %{_infodir}/standards.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/autoconf.1*
%attr(0644,root,root) %{_mandir}/man1/autoheader.1*
%attr(0644,root,root) %{_mandir}/man1/autom4te.1*
%attr(0644,root,root) %{_mandir}/man1/autoreconf.1*
%attr(0644,root,root) %{_mandir}/man1/autoscan.1*
%attr(0644,root,root) %{_mandir}/man1/autoupdate.1*
%attr(0644,root,root) %{_mandir}/man1/ifnames.1*
%license COPYING COPYING.EXCEPTION COPYINGv3
%doc AUTHORS BUGS COPYING COPYING.EXCEPTION COPYINGv3 NEWS README THANKS TODO
%doc %{name}-make.check.log



%changelog
* Sat May 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.44-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
