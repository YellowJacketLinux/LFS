%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     readline
Version:  8.2
Release:  %{?repo}0.rc2%{?dist}
Summary:  Library for editing typed command lines

Group:    System Environment/Libraries
License:  GPLv3
URL:      https://tiswww.case.edu/php/chet/readline/rltop.html
Source0:  https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Patch0:   https://www.linuxfromscratch.org/patches/lfs/11.3/%{name}-%{version}-upstream_fix-1.patch

BuildRequires:    pkgconfig(ncurses)
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}	

%description
The Readline library provides a set of functions for use by applications
that allow users to edit command lines as they are typed in.  Both
Emacs and vi editing modes are available.  The Readline library includes
additional functions to maintain a list of previously-entered command
lines, to recall and perhaps reedit those lines, and perform csh-like
history expansion on previous commands.

The history facilities are also placed into a separate library, the
History library, as part of the build process.  The History library may
be used without Readline in applications which desire its capabilities.

%package devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(ncurses)

%description devel
This package includes the developer files needed to develop software
that links against the libreadline and libhistory libraries.

%prep
%setup -q
%patch 0 -p1

%build
%configure \
  --libdir=/%{_lib} \
  --disable-static \
  --with-curses
make %{?_smp_mflags} SHLIB_LIBS="-lncursesw"

%install
make SHLIB_LIBS="-lncursesw" DESTDIR=%{buildroot} install

# fix pkgconfig files
sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/readline.pc
sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}/%{_lib}/pkgconfig/history.pc
[ ! -d %{buildroot}%{_libdir} ] && mkdir -p %{buildroot}%{_libdir}
mv %{buildroot}/lib/pkgconfig %{buildroot}%{_libdir}/
rm -f %{buildroot}/%{_lib}/libhistory.so
rm -f %{buildroot}/%{_lib}/libreadline.so

ln -sf ../../%{_lib}/libhistory.so.8.2 %{buildroot}%{_libdir}/libhistory.so
ln -sf ../../%{_lib}/libreadline.so.8.2 %{buildroot}%{_libdir}/libreadline.so

# remove installed docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%post
/sbin/ldconfig
%{insinfo} %{_infodir}/history.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/readline.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/rluserman.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/history.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/readline.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/rluserman.info %{_infodir}/dir ||:
fi

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) /lib/libhistory.so.8.2
/lib/libhistory.so.8
%attr(0755,root,root) /lib/libreadline.so.8.2
/lib/libreadline.so.8
%exclude %{_infodir}/dir
%{_infodir}/history.info*
%{_infodir}/readline.info*
%{_infodir}/rluserman.info*
%doc CHANGELOG CHANGES COPYING NEWS README
%doc doc/*.ps doc/*.pdf doc/*.html doc/*.dvi
%license COPYING

%files devel
%defattr(-,root,root,-)
%{_includedir}/readline
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%attr(0644,root,root) %{_mandir}/man3/history.3*
%attr(0644,root,root) %{_mandir}/man3/readline.3*
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license COPYING

%changelog
* Wed Apr 12 2023 Michael A. Peters <anymouseprophet@gmail.com> - 8.2-0.rc2
- Rebuild with newly packaged gcc

* Mon Mar 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 8.2-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
