%global zipv 3.0
%global nodotzipv 30

Name:     zip
Version:  %{zipv}
Release:  %{?dist}0.rc1%{?dist}
Summary:  Utilities for creating .zip archives

Group:    System Environment/Utilities
License:  Info-ZIP
URL:      https://infozip.sourceforge.net/Zip.html
Source0:  https://downloads.sourceforge.net/infozip/zip%{nodotzipv}.tar.gz

BuildRequires:  libbz2-devel

%description
Zip is useful for packaging a set of files for distribution, for archiving
files, and for saving disk space by temporarily compressing unused files
or directories. Zip puts one or more compressed files into a single ZIP
archive, along with information about the files (name, path, date, time
of last modification, protection, and check information to verify file
integrity). An entire directory structure can be packed into a ZIP
archive with a single command.

Zip has one compression method (deflation) and can also store files
without compression. Zip automatically chooses the better of the two
for each file. Compression ratios of 2:1 to 3:1 are common for text
files. 

%prep
%setup -q -n %{name}%{nodotzipv}


%build
make %{?_smp_mflags} -f unix/Makefile generic_gcc


%install
make prefix=%{buildroot}%{_prefix}      \
     MANDIR=%{buildroot}%{_mandir}/man1 \
  -f unix/Makefile install


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/zip
%attr(0755,root,root) %{_bindir}/zipcloak
%attr(0755,root,root) %{_bindir}/zipnote
%attr(0755,root,root) %{_bindir}/zipsplit
%attr(0644,root,root) %{_mandir}/man1/zip.1*
%attr(0644,root,root) %{_mandir}/man1/zipcloak.1*
%attr(0644,root,root) %{_mandir}/man1/zipnote.1*
%attr(0644,root,root) %{_mandir}/man1/zipsplit.1*
%license LICENSE
%doc BUGS CHANGES LICENSE README* TODO WHATSNEW



%changelog
* Mon May 1 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
