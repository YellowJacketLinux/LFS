# Many (most?) distributions put install-info in /{,usr/}sbin
#  YJL defines this macro to /usr/bin/install-info
#  so define it to be in /sbin/ if not defined.
%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     m4
Version:  1.4.19
Release:  %{?repo}0.rc2%{?dist}
Summary:  Unix macro processor

Group:    Development/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/m4/
Source0:	https://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz

#BuildRequires:	
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
GNU M4 is an implementation of the traditional Unix macro processor.
It is mostly SVR4 compatible although it has some extensions (for
example, handling more than 9 positional parameters to macros). GNU M4
also has built-in functions for including files, running shell commands,
doing arithmetic, etc.

GNU M4 is a macro processor in the sense that it copies its input to
the output expanding macros as it goes. Macros are either builtin or
user-defined and can take any number of arguments. Besides just doing
macro expansion, m4 has builtin functions for including named files,
running UNIX commands, doing integer arithmetic, manipulating text in
various ways, recursion etc... m4 can be used either as a front-end to
a compiler or as a macro processor in its own right.

One of the biggest users of GNU M4 is the GNU Autoconf project. 

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%check
make check > m4-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang m4

%post
%{insinfo} %{_infodir}/m4.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/m4.info %{_infodir}/dir || :
fi

%files -f m4.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/m4
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/m4.info*
%attr(0644,root,root) %{_mandir}/man1/m4.1*
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%doc m4-make.check.log


%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.4.19-0.rc2
- Rebuild with newly packaged gcc

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 1.4.19-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
