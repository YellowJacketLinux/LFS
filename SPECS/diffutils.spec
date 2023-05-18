%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     diffutils
Version:  3.9
Release:	%{?repo}0.rc1%{?dist}
Summary:  programs related to finding differences between files

Group:    System Environment/Utilities
License:  GPL-3.0-or-later
URL:      https://www.gnu.org/software/diffutils/
Source0:  https://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz

#BuildRequires:
Requires(post):   %{insinfo}
Requires(postun): %{insinfo}

%description
GNU Diffutils is a package of several programs related to finding
differences between files.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run at package build" > %{name}-make.check.log
%endif


%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%post
%{insinfo} %{_infodir}/diffutils.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/diffutils.info %{_infodir}/dir ||:
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/cmp
%attr(0755,root,root) %{_bindir}/diff
%attr(0755,root,root) %{_bindir}/diff3
%attr(0755,root,root) %{_bindir}/sdiff
%attr(0644,root,root) %{_infodir}/diffutils.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/cmp.1*
%attr(0644,root,root) %{_mandir}/man1/diff.1*
%attr(0644,root,root) %{_mandir}/man1/diff3.1*
%attr(0644,root,root) %{_mandir}/man1/sdiff.1*
%license COPYING
%doc AUTHORS ChangeLog* COPYING NEWS README THANKS TODO
%doc %{name}-make.check.log



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.9-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
