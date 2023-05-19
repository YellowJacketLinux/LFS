%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     findutils
Version:  4.9.0
Release:	%{?repo}0.rc1%{?dist}
Summary:  basic directory searching utilities

Group:    System Environment/Utilities
License:  GPL-3.0-or-later
URL:      https://www.gnu.org/software/findutils/
Source0:  https://ftp.gnu.org/gnu/findutils/findutils-%{version}.tar.xz

BuildRequires:    libpcre2-devel
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
The GNU Find Utilities are the basic directory searching utilities of
the GNU operating system. These programs are typically used in conjunction
with other programs to provide modular and powerful directory search and
file locating capabilities to other commands.

%prep
%setup -q


%build
%configure \
  --localstatedir=%{_sharedstatedir}/locate
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" > %{name}-make.check.log
%endif

%post
%{insinfo} %{_infodir}/find-maint.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/find.info %{_infodir}/dir ||:


%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/find-maint.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/find.info %{_infodir}/dir ||:
fi

%install
make install DESTDIR=%{buildroot}
%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/find
%exclude %{_bindir}/locate
%exclude %{_bindir}/updatedb
%attr(0755,root,root) %{_bindir}/xargs
%attr(0755,root,root) %{_libexecdir}/frcode
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/find-maint.info*
%attr(0644,root,root) %{_infodir}/find.info*
%attr(0644,root,root) %{_mandir}/man1/find.1*
%exclude %{_mandir}/man1/locate.1*
%exclude %{_mandir}/man1/updatedb.1*
%attr(0644,root,root) %{_mandir}/man1/xargs.1*
%exclude %{_mandir}/man5/locatedb.5*
#%%dir %%{_sharedstatedir}/locate
%license COPYING
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO
%doc %{name}-make.check.log



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 4.9.0-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
- Not packaging locate or updatedb (using plocate for them)
