%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     sed
Version:  4.9
Release:  %{?repo}2%{?dist}
Summary:  A non-interactive command-line text editor

Group:    System Environment/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/sed/
Source0:  https://ftp.gnu.org/gnu/sed/sed-%{version}.tar.xz

BuildRequires:  libattr-devel
BuildRequires:  libacl-devel
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
The `sed' command is commonly used to filter text, i.e., it takes text
input, performs some operation (or set of operations) on it, and outputs
the modified text.

The `sed' command is typocally used for extracting part of a file using
pattern matching or substituting multiple occurrences of a string within
a file.

%prep
%setup -q

%build
%configure --bindir=/bin
make %{?_smp_mflags}
make html

%check
make check > sed-make.check.log 2>&1

%install
make install DESTDIR=%{buildroot}
%find_lang sed

%post
%{insinfo} %{_infodir}/sed.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/sed.info %{_infodir}/dir ||:
fi

%files -f sed.lang
%defattr(-,root,root,-)
%attr(0755,root,root) /bin/sed
%attr(0644,root,root) %{_infodir}/sed.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/sed.1*
%license COPYING
%doc AUTHORS BUGS COPYING ChangeLog README NEWS THANKS
%doc doc/sed.html sed-make.check.log



%changelog
* Mon Apr 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.9-2
- Rebuild with newly packaged gcc, fix install-info scriptlets

* Wed Mar 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.9-1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
