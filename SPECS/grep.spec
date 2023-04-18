%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     grep
Version:  3.8
Release:  %{?repo}0.rc1%{?dist}
Summary:  text pattern matching utility

Group:    System Environment/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/grep/
Source0:  https://ftp.gnu.org/gnu/grep/grep-%{version}.tar.xz

#BuildRequires:
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
Grep searches one or more input files for lines containing a match to
a specified pattern. By default, Grep outputs the matching lines.

%prep
%setup -q
sed -i "s/echo/#echo/" src/egrep.sh

%build
%configure
make %{?_smp_mflags}

%check
make check > %{name}-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang grep

%post
%{insinfo} %{_infodir}/%{name}.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/%{name}.info %{_infodir}/dir ||:
fi

%files -f grep.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/egrep
%attr(0755,root,root) %{_bindir}/fgrep
%attr(0755,root,root) %{_bindir}/grep
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/grep.info*
%attr(0644,root,root) %{_mandir}/man1/grep.1*
%license COPYING
%doc %{name}-make.check.log
%doc AUTHORS COPYING ChangeLog* COPYING NEWS README THANKS TODO


%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.8-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
