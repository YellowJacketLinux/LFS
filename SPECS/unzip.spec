%global unzipv 6.0
%global nodotunzipv 60

Name:     unzip
Version:  %{unzipv}
Release:  %{?repo}0.rc1%{?dist}
Summary:  List, test, extract files from a .zip archive

Group:    System Environment/Utilities
License:  Info-ZIP
URL:      https://infozip.sourceforge.net/UnZip.html
Source0:  https://downloads.sourceforge.net/infozip/unzip%{nodotunzipv}.tar.gz
Patch0:   https://www.linuxfromscratch.org/patches/blfs/11.3/unzip-6.0-consolidated_fixes-1.patch

BuildRequires:  libbz2-devel

%description
UnZip is an extraction utility for archives compressed in .zip format
(also called "zipfiles"). Although highly compatible both with PKWARE's
PKZIP and PKUNZIP utilities for MS-DOS and with Info-ZIP's own Zip
program, our primary objectives have been portability and non-MSDOS
functionality.


%prep
%setup -q -n %{name}%{nodotunzipv}
%patch 0 -p1

%build
make %{?_smp_mflags} -f unix/Makefile generic


%install
make prefix=%{buildroot}%{_prefix}      \
     MANDIR=%{buildroot}%{_mandir}/man1 \
  -f unix/Makefile install


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/funzip
%attr(0755,root,root) %{_bindir}/unzip
%attr(0755,root,root) %{_bindir}/unzipsfx
%attr(0755,root,root) %{_bindir}/zipgrep
%attr(0755,root,root) %{_bindir}/zipinfo
%attr(0644,root,root) %{_mandir}/man1/funzip.1*
%attr(0644,root,root) %{_mandir}/man1/unzip.1*
%attr(0644,root,root) %{_mandir}/man1/unzipsfx.1*
%attr(0644,root,root) %{_mandir}/man1/zipgrep.1*
%attr(0644,root,root) %{_mandir}/man1/zipinfo.1*
%license LICENSE COPYING.OLD
%doc BUGS COPYING.OLD LICENSE README ToDo



%changelog
* Mon May 1 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
