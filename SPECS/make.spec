# Some distributions put install-info in /{,usr/}sbin
%global insinfo %{_bindir}/install-info

Name:		make
Version:	4.4
Release:	%{?repo}0.rc1%{?dist}
Summary:	Utility for building from a makefile

Group:		Development/Utilities
License:	GPLv3
URL:		https://www.gnu.org/software/make/
Source0:	https://ftp.gnu.org/gnu/make/make-%{version}.tar.gz

#BuildRequires:	
Requires(post):	%{insinfo}
Requires(preun):	%{insinfo}

%description
GNU Make is a tool which controls the generation of executables and
other non-source files of a program from the program's source files.

%prep
%setup -q
sed -e '/ifdef SIGPIPE/,+2 d' \
    -e '/undef  FATAL_SIG/i FATAL_SIG (SIGPIPE);' \
    -i src/main.c


%build
%configure
make %{?_smp_mflags}

%check
make check > make-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%post
%{insinfo} %{_infodir}/make.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/make.info %{_infodir}/dir ||:
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/make
%attr(0644,root,root) %{_includedir}/gnumake.h
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/make.info*
%attr(0644,root,root) %{_mandir}/man1/make.1*
%license COPYING
%doc AUTHORS ChangeLog COPYING make-make.check.log


%changelog
* Mon Apr 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.4-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)

