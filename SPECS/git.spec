# FIXME - man pages needs put into subpackages

%global specrel 0.dev2

# no stripping
%global debug_package %{nil}
%global __strip /bin/true

%global gitdocs %{_datadir}/git-documentation

%if 0%{?!__tar:1} == 1
%global __tar %{_bindir}/tar}
%endif
%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed}
%endif

%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
%global novalgrind  novalgrind
%global notk        notk
%endif
%if "%{repo}" == "2.cli."
%global notk        notk
%endif
%endif

Name:     git
Version:  2.40.1
Release:  %{?repo}%{specrel}%{?dist}
Summary:  distributed version control system

Group:    Development/Utilities
License:  GPL-2.0-only and LGPL-2.1-or-later
URL:      https://git-scm.com/
Source0:  https://www.kernel.org/pub/software/scm/git/git-%{version}.tar.xz
Source1:  https://www.kernel.org/pub/software/scm/git/git-manpages-%{version}.tar.xz
Source2:  https://www.kernel.org/pub/software/scm/git/git-htmldocs-%{version}.tar.xz

BuildRequires:  %{__tar}
BuildRequires:  %{__sed}
BuildRequires:  perl-devel
BuildRequires:  python3-devel
BuildRequires:  libpcre2-devel
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib)
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
%if 0%{?!notk:1} == 1
BuildRequires:  tk-devel
%endif
%if 0%{?runtests:1} == 1
%if 0%{?!novalgrind:1} == 1
BuildRequires:  valgrind
%endif
%endif
Requires: curl
Requires: openssh-clients
Requires: perl-Git = %{version}-%{release}


%description
Git is a free and open source distributed version control system designed
to handle everything from small to very large projects with speed and
efficiency.

Git is easy to learn and has a tiny footprint with lightning fast
performance. It outclasses SCM tools like Subversion, CVS, Perforce,
and ClearCase with features like cheap local branching, convenient
staging areas, and multiple workflows.

%package -n perl-Git
Group:    Development/Libraries
Summary:  Git Perl modules
BuildArch:  noarch
Requires: %{name} = %{version}-%{release}
%if 0%{?perl5_API:1} == 1
Requires: %{perl5_API}
%endif

%description -n perl-Git
This package contains the Git perl modules.

%if 0%{?!notk:1} == 1
%package gui
Group:    Applications/Development
Summary:  The Tcl/Tk GUI front-end to git
Requires: %{name} = %{version}-%{release}
BuildRequires:  tk-devel
Requires: tk
BuildArch:  noarch

%description gui
This package provides the Tcl/Tk graphical front-end to git.
%endif

%package documentation
Group:    Developer/Documentation
Summary:  HTML and Text documentation for git
Requires: %{name} = %{version}-%{release}
BuildArch:  noarch

%description documentation
This package contains the in-depth HTML and Text documentation for git.

%prep
%setup -q


%build
%configure \
  --with-gitconfig=%{_sysconfdir}/gitconfig \
%if 0%{?notk:1} == 1
  --with-tcltk=no \
%endif
  --with-perl=%{__perl} \
  --with-python=%{python3}
make %{?_smp_mflags}


%check
%if 0%{?runtests:1} == 1
make test > %{name}-make.test.log 2>&1
%else
echo "make test not run at package build" > %{name}-make.test.log
%endif

%install
make perllibdir=%{perl5_vendorlib} install DESTDIR=%{buildroot}
install -m644 -D contrib/completion/git-completion.bash \
  %{buildroot}%{_datadir}/bash-completion/completions/git
%find_lang git

[ ! -d %{buildroot}%{_mandir} ] && mkdir -p %{buildroot}%{_mandir}
%{__tar} -xf %{SOURCE1} \
  -C %{buildroot}%{_mandir} --no-same-owner --no-overwrite-dir
mkdir -p %{buildroot}%{gitdocs}
%{__tar} -xf %{SOURCE2} \
  -C %{buildroot}%{gitdocs} --no-same-owner --no-overwrite-dir
find %{buildroot}%{gitdocs} -type d -exec chmod 755 {} \;
find %{buildroot}%{gitdocs} -type f -exec chmod 644 {} \;

# reorganize html docs
mkdir -p %{buildroot}%{gitdocs}/man-pages/{html,text}
mv %{buildroot}%{gitdocs}/{git*.txt,man-pages/text}
mv %{buildroot}%{gitdocs}/{git*.,index.,man-pages/}html
mkdir -p %{buildroot}%{gitdocs}/technical/{html,text}
mv %{buildroot}%{gitdocs}/technical/{*.txt,text}
mv %{buildroot}%{gitdocs}/technical/{*.,}html
mkdir -p %{buildroot}%{gitdocs}/howto/{html,text}
mv %{buildroot}%{gitdocs}/howto/{*.txt,text}
mv %{buildroot}%{gitdocs}/howto/{*.,}html
%__sed -i '/^<a href=/s|howto/|&html/|' %{buildroot}%{gitdocs}/howto-index.html
%__sed -i '/^\* link:/s|howto/|&html/|' %{buildroot}%{gitdocs}/howto-index.txt


%files -f git.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/git
%attr(0755,root,root) %{_bindir}/git-cvsserver
%attr(0755,root,root) %{_bindir}/git-receive-pack
%attr(0755,root,root) %{_bindir}/git-shell
%attr(0755,root,root) %{_bindir}/git-upload-archive
%attr(0755,root,root) %{_bindir}/git-upload-pack
%attr(0755,root,root) %{_bindir}/scalar
%{_libexecdir}/git-core
%{_datadir}/git-core
%attr(0644,root,root) %{_datadir}/bash-completion/completions/git
#
%{_datadir}/gitweb
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man7/*.7*
%license COPYING LGPL-2.1
%doc COPYING README.md SECURITY.md
%doc %{name}-make.test.log

# fixme - these belong is vendor-perl
%files -n perl-Git
%defattr(-,root,root,-)
%dir %{perl5_vendorlib}/FromCPAN
%attr(0444,root,root) %{perl5_vendorlib}/FromCPAN/Error.pm
%dir %{perl5_vendorlib}/FromCPAN/Mail
%attr(0444,root,root) %{perl5_vendorlib}/FromCPAN/Mail/Address.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git.pm
%dir %{perl5_vendorlib}/Git
%attr(0444,root,root) %{perl5_vendorlib}/Git/I18N.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/IndexInfo.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/LoadCPAN.pm
%dir %{perl5_vendorlib}/Git/LoadCPAN
%attr(0444,root,root) %{perl5_vendorlib}/Git/LoadCPAN/Error.pm
%dir %{perl5_vendorlib}/Git/LoadCPAN/Mail
%attr(0444,root,root) %{perl5_vendorlib}/Git/LoadCPAN/Mail/Address.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/Packet.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN.pm
%dir %{perl5_vendorlib}/Git/SVN
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Editor.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Fetcher.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/GlobSpec.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Log.pm
%dir %{perl5_vendorlib}/Git/SVN/Memoize
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Memoize/YAML.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Migration.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Prompt.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Ra.pm
%attr(0444,root,root) %{perl5_vendorlib}/Git/SVN/Utils.pm
%license COPYING LGPL-2.1

%if 0%{?!notk:1} == 1
%files gui
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gitk
%dir %{_datadir}/git-gui
%dir %{_datadir}/git-gui/lib
%{_datadir}/git-gui/lib/*.tcl
%{_datadir}/git-gui/lib/*.js
%{_datadir}/git-gui/lib/git-gui.ico
%{_datadir}/git-gui/lib/tclIndex
%dir %{_datadir}/git-gui/lib/msgs
%lang(bg) %{_datadir}/git-gui/lib/msgs/bg.msg
%lang(de) %{_datadir}/git-gui/lib/msgs/de.msg
%lang(el) %{_datadir}/git-gui/lib/msgs/el.msg
%lang(fr) %{_datadir}/git-gui/lib/msgs/fr.msg
%lang(hu) %{_datadir}/git-gui/lib/msgs/hu.msg
%lang(it) %{_datadir}/git-gui/lib/msgs/it.msg
%lang(ja) %{_datadir}/git-gui/lib/msgs/ja.msg
%lang(nb) %{_datadir}/git-gui/lib/msgs/nb.msg
%lang(pt_br) %{_datadir}/git-gui/lib/msgs/pt_br.msg
%lang(pt_pt) %{_datadir}/git-gui/lib/msgs/pt_pt.msg
%lang(ru) %{_datadir}/git-gui/lib/msgs/ru.msg
%lang(sv) %{_datadir}/git-gui/lib/msgs/sv.msg
%lang(vi) %{_datadir}/git-gui/lib/msgs/vi.msg
%lang(zh_cn) %{_datadir}/git-gui/lib/msgs/zh_cn.msg
%dir %{_datadir}/gitk
%dir %{_datadir}/gitk/lib
%dir %{_datadir}/gitk/lib/msgs
%lang(bg) %{_datadir}/gitk/lib/msgs/bg.msg
%lang(ca) %{_datadir}/gitk/lib/msgs/ca.msg
%lang(de) %{_datadir}/gitk/lib/msgs/de.msg
%lang(es) %{_datadir}/gitk/lib/msgs/es.msg
%lang(fr) %{_datadir}/gitk/lib/msgs/fr.msg
%lang(hu) %{_datadir}/gitk/lib/msgs/hu.msg
%lang(it) %{_datadir}/gitk/lib/msgs/it.msg
%lang(ja) %{_datadir}/gitk/lib/msgs/ja.msg
%lang(pt_br) %{_datadir}/gitk/lib/msgs/pt_br.msg
%lang(pt_pt) %{_datadir}/gitk/lib/msgs/pt_pt.msg
%lang(ru) %{_datadir}/gitk/lib/msgs/ru.msg
%lang(sv) %{_datadir}/gitk/lib/msgs/sv.msg
%lang(vi) %{_datadir}/gitk/lib/msgs/vi.msg
%lang(zh_cn) %{_datadir}/gitk/lib/msgs/zh_cn.msg
%license COPYING LGPL-2.1
%doc COPYING README.md SECURITY.md
%endif

%files documentation
%defattr(-,root,root,-)
%license COPYING
%{gitdocs}


%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.40.1-0.dev2
- Add bash completion file

* Sat May 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.40.1-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
