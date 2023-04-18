Name:     ncurses
Version:  6.4
Release:  %{?repo}0.rc3%{?dist}
Summary:  The ncurses library

Group:    System Environment/Libraries
License:  MIT
URL:      https://invisible-island.net/ncurses/ncurses.html
Source0:  https://invisible-mirror.net/archives/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  libstdc++-devel

%description
The ncurses library.

%package -n ada-ncurses
Summary:  Ada support files for ncurses
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildRequires:  gcc-gnat

# FIXME
%description -n ada-ncurses
This package contains some ada support files that I still need to
properly investigate and understand the purpose of.

%package devel
Summary:  Development files for ncurses
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to build software that links
against the ncurses library.

%prep
%setup -q

%build
%configure          \
  --libdir=/lib     \
  --with-shared     \
  --without-debug   \
  --without-normal  \
  --with-cxx-shared \
  --enable-pc-files \
  --enable-widec    \
  --with-pkg-config-libdir=%{_libdir}/pkgconfig
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

for PC in formw.pc menuw.pc ncurses++w.pc ncursesw.pc panelw.pc; do
  sed -i 's?^libdir=.*?libdir=%{_libdir}?' %{buildroot}%{_libdir}/pkgconfig/${PC}
  sed -i 's?-L/lib?-L%{_libdir}?' %{buildroot}%{_libdir}/pkgconfig/${PC}
done

rm -f %{buildroot}/%{_lib}/libformw.so
ln -sf ../../%{_lib}/libformw.so.6 %{buildroot}%{_libdir}/libformw.so
rm -f %{buildroot}/%{_lib}/libmenuw.so
ln -sf ../../%{_lib}/libmenuw.so.6 %{buildroot}%{_libdir}/libmenuw.so
rm -f %{buildroot}/%{_lib}/libncurses++w.so
ln -sf ../../%{_lib}/libncurses++w.so.6 %{buildroot}%{_libdir}/libncurses++w.so
rm -f %{buildroot}/%{_lib}/libncursesw.so
ln -sf ../../%{_lib}/libncursesw.so.6 %{buildroot}%{_libdir}/libncursesw.so
rm -f %{buildroot}/%{_lib}/libpanelw.so
ln -sf ../../%{_lib}/libpanelw.so.6 %{buildroot}%{_libdir}/libpanelw.so

### hackery...

# create non-wide variants
for lib in ncurses form panel menu ; do
  echo "INPUT(-l${lib}w)" > %{buildroot}%{_libdir}/lib${lib}.so
  ln -sfv ${lib}w.pc        %{buildroot}%{_libdir}/pkgconfig/${lib}.pc
done

# for libcurses / libcuresesw compatibility
echo "INPUT(-lncursesw)" > %{buildroot}%{_libdir}/libcursesw.so
ln -sfv libncurses.so      %{buildroot}%{_libdir}/libcurses.so

### /end hackery...

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/clear
%attr(0755,root,root) %{_bindir}/infocmp
%attr(0755,root,root) %{_bindir}/ncursesw6-config
%attr(0755,root,root) %{_bindir}/tabs
%attr(0755,root,root) %{_bindir}/tic
%attr(0755,root,root) %{_bindir}/toe
%attr(0755,root,root) %{_bindir}/tput
%attr(0755,root,root) %{_bindir}/tset
%{_bindir}/captoinfo
%{_bindir}/infotocap
%{_bindir}/reset
/lib/libformw.so.6
%attr(0755,root,root) /lib/libformw.so.6.4
/lib/libmenuw.so.6
%attr(0755,root,root) /lib/libmenuw.so.6.4
/lib/libncurses++w.so.6
%attr(0755,root,root) /lib/libncurses++w.so.6.4
/lib/libncursesw.so.6
%attr(0755,root,root) /lib/libncursesw.so.6.4
/lib/libpanelw.so.6
%attr(0755,root,root) /lib/libpanelw.so.6.4
%{_datadir}/tabset
%{_datadir}/terminfo
%attr(0644,root,root) %{_mandir}/man1/captoinfo.1m*
%attr(0644,root,root) %{_mandir}/man1/clear.1*
%attr(0644,root,root) %{_mandir}/man1/infocmp.1m*
%attr(0644,root,root) %{_mandir}/man1/infotocap.1m*
%attr(0644,root,root) %{_mandir}/man1/ncursesw6-config.1*
%attr(0644,root,root) %{_mandir}/man1/tabs.1*
%attr(0644,root,root) %{_mandir}/man1/tic.1m*
%attr(0644,root,root) %{_mandir}/man1/toe.1m*
%attr(0644,root,root) %{_mandir}/man1/tput.1*
%attr(0644,root,root) %{_mandir}/man1/tset.1*
%{_mandir}/man1/reset.1*
%attr(0644,root,root) %{_mandir}/man5/*
%attr(0644,root,root) %{_mandir}/man7/*
%doc ANNOUNCE AUTHORS COPYING NEWS README TO-DO 
%license COPYING

%files -n ada-ncurses
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/adacursesw6-config
%attr(0755,root,root) %dir %{_libdir}/ada
%attr(0755,root,root) %dir %{_libdir}/ada/adalib
%attr(0644,root,root) %{_libdir}/ada/adalib/libAdaCurses.a
%attr(0755,root,root) %dir %{_datadir}/ada
%attr(0755,root,root) %dir %{_datadir}/ada/adainclude
%attr(0644,root,root) %{_datadir}/ada/adainclude/*.adb
%attr(0644,root,root) %{_datadir}/ada/adainclude/*.ads
%attr(0644,root,root) %{_mandir}/man1/adacursesw6-config.1*
%{_mandir}/man1/adacursesw6.1*

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/libcursesw.so
%attr(0644,root,root) %{_libdir}/libform.so
%attr(0644,root,root) %{_libdir}/libmenu.so
%attr(0644,root,root) %{_libdir}/libncurses.so
%attr(0644,root,root) %{_libdir}/libpanel.so
%{_libdir}/libcurses.so
%{_libdir}/libformw.so
%{_libdir}/libmenuw.so
%{_libdir}/libncurses++w.so
%{_libdir}/libncursesw.so
%{_libdir}/libpanelw.so
%attr(0644,root,root) %{_libdir}/pkgconfig/formw.pc
%attr(0644,root,root) %{_libdir}/pkgconfig/menuw.pc
%attr(0644,root,root) %{_libdir}/pkgconfig/ncurses++w.pc
%attr(0644,root,root) %{_libdir}/pkgconfig/ncursesw.pc
%attr(0644,root,root) %{_libdir}/pkgconfig/panelw.pc
%{_libdir}/pkgconfig/form.pc
%{_libdir}/pkgconfig/menu.pc
%{_libdir}/pkgconfig/ncurses.pc
%{_libdir}/pkgconfig/panel.pc
%{_includedir}/*.h
%{_mandir}/man3/*.3*
%doc doc/hackguide.doc
%doc doc/html
%doc doc/ncurses-intro.doc



%changelog
* Tue Mar 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.4-0.rc2
- Some spec file cleanup, ada files

* Mon Mar 13 2023 Michael A. Peters <anymouseprophet@gmail.com> - 6.4-0.rc1
- Initial spec file
