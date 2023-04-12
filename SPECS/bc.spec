Name:     bc
Version:  6.2.4
Release:  %{?repo}0.rc2%{?dist}
Summary:  Arbitrary precision numeric processing language

Group:    System Environment/Utilities
License:  MIT
URL:      https://git.gavinhoward.com/gavin/bc
Source0:  https://github.com/gavinhoward/bc/releases/download/%{version}/bc-%{version}.tar.xz

BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
#Requires:	

%description
An implementation of Unix dc and POSIX bc with GNU and BSD extensions.
Finished, but well-maintained

This is an implementation of the POSIX bc calculator that implements
GNU bc extensions, as well as the period (.) extension for the BSD
flavor of bc.

For more information, see this bc's full manual.

This bc also includes an implementation of dc in the same binary,
accessible via a symbolic link, which implements all FreeBSD and GNU
extensions. The ! command is omitted; I believe this poses security
concerns and that such functionality is unnecessary.

For more information, see the dc's full manual.

%prep
%setup -q

%build
CC=gcc ./configure --prefix=%{_prefix} -G -O3 -r
make %{?_smp_mflags}

%check
make test > bc-make.test.log 2>&1

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/bc
%{_bindir}/dc
%attr(0644,root,root) %{_mandir}/man1/bc.1*
%attr(0644,root,root) %{_mandir}/man1/dc.1*
%lang(de_AT) %{_datadir}/locale/de_AT.*
%lang(de_CH) %{_datadir}/locale/de_CH.*
%lang(de_DE) %{_datadir}/locale/de_DE.*
%lang(en_AU) %{_datadir}/locale/en_AU.*
%lang(en_CA) %{_datadir}/locale/en_CA.*
%lang(en_GB) %{_datadir}/locale/en_GB.*
%lang(en_IE) %{_datadir}/locale/en_IE.*
%lang(en_NZ) %{_datadir}/locale/en_NZ.*
%lang(en_US) %{_datadir}/locale/en_US.*
%lang(en_US) %{_datadir}/locale/en_US
%lang(es_ES) %{_datadir}/locale/es_ES.*
%lang(fr_BE) %{_datadir}/locale/fr_BE.*
%lang(fr_CA) %{_datadir}/locale/fr_CA.*
%lang(fr_CH) %{_datadir}/locale/fr_CH.*
%lang(fr_FR) %{_datadir}/locale/fr_FR.*
%lang(ja_JP) %{_datadir}/locale/ja_JP.*
%lang(nl_NL) %{_datadir}/locale/nl_NL.*
%lang(pl_PL) %{_datadir}/locale/pl_PL.*
%lang(pt_BR) %{_datadir}/locale/pt_BR.*
%lang(pt_PT) %{_datadir}/locale/pt_PT.*
%lang(ru_RU) %{_datadir}/locale/ru_RU.*
%lang(zh_CN) %{_datadir}/locale/zh_CN.*
%license LICENSE.md
%doc LICENSE.md MEMORY_BUGS.md NEWS.md NOTICE.md README.md
%doc bc-make.test.log


%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.4-0.rc2
- Rebuild with freshly packaged gcc

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.2.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
