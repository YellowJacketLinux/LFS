Name:     glib2
Version:  2.76.0
Release:  %{?repo}0.rc2%{?dist}
Summary:  Glib 2 libraries

Group:    System Environment/Libraries
License:  LGPLv2.1
URL:      https://wiki.gnome.org/Projects/GLib
Source0:  https://download.gnome.org/sources/glib/2.76/glib-2.76.0.tar.xz

BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  libpcre2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(blkid)
BuildRequires:  util-linux-devel
BuildRequires:  pkgconfig(libelf)
BuildRequires:  meson >= 0.60.0
BuildRequires:  ninja

%description
GLib provides the core application building blocks for libraries and
applications written in C. It provides the core object system used in
GNOME, the main loop implementation, and a large set of utility
functions for strings and common data structures.

%package devel
Summary:	GLib 2 development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the developer files needed to build software that links
against GLib 2.

%prep
%setup -q -n glib-%{version}


%build
mkdir build && cd build

meson setup --prefix=/usr       \
      --buildtype=release 
#      -Dman=true          

ninja


%install
cd build
export DESTDIR=%{buildroot}
ninja install
%find_lang glib20

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f build/glib20.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libgio-2.0.so.0.7600.0
%{_libdir}/libgio-2.0.so.0
%attr(0755,root,root) %{_libdir}/libglib-2.0.so.0.7600.0
%{_libdir}/libglib-2.0.so.0
%attr(0755,root,root) %{_libdir}/libgmodule-2.0.so.0.7600.0
%{_libdir}/libgmodule-2.0.so.0
%attr(0755,root,root) %{_libdir}/libgobject-2.0.so.0.7600.0
%{_libdir}/libgobject-2.0.so.0
%attr(0755,root,root) %{_libdir}/libgthread-2.0.so.0.7600.0
%{_libdir}/libgthread-2.0.so.0
%license COPYING NEWS README.md SECURITY.md
%doc COPYING NEWS README.md SECURITY.md

%files devel
%defattr(-,root,root,-)
%{_bindir}/*
%{_libexecdir}/gio-launch-desktop
%attr(0644,root,root) %{_datadir}/bash-completion/completions/gapplication
%attr(0644,root,root) %{_datadir}/bash-completion/completions/gdbus
%attr(0644,root,root) %{_datadir}/bash-completion/completions/gio
%attr(0644,root,root) %{_datadir}/bash-completion/completions/gresource
%attr(0644,root,root) %{_datadir}/bash-completion/completions/gsettings
%{_datadir}/glib-2.0
%{_datadir}/gettext/its/gschema.*
%{_datadir}/gdb/auto-load/usr/lib/*.py
%dir %{_includedir}/gio-unix-2.0
%dir %{_includedir}/gio-unix-2.0/gio
%attr(0644,root,root) %{_includedir}/gio-unix-2.0/gio/*.h
%dir %{_includedir}/glib-2.0
%attr(0644,root,root) %{_includedir}/glib-2.0/*.h
%dir %{_includedir}/glib-2.0/gio
%attr(0644,root,root) %{_includedir}/glib-2.0/gio/*.h
%dir %{_includedir}/glib-2.0/glib
%attr(0644,root,root) %{_includedir}/glib-2.0/glib/*.h
%dir %{_includedir}/glib-2.0/glib/deprecated
%attr(0644,root,root) %{_includedir}/glib-2.0/glib/deprecated/*.h
%dir %{_includedir}/glib-2.0/gmodule
%attr(0644,root,root) %{_includedir}/glib-2.0/gmodule/gmodule-visibility.h
%dir %{_includedir}/glib-2.0/gobject
%attr(0644,root,root) %{_includedir}/glib-2.0/gobject/*.h
%attr(0644,root,root) %{_includedir}/glib-2.0/gobject/gobjectnotifyqueue.c
%{_libdir}/glib-2.0
%{_libdir}/*.so
%attr(0644,root,root) %{_datadir}/aclocal/*.m4
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc
%license COPYING
%doc COPYING NEWS README.md SECURITY.md

%changelog
* Thu May 11 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.76.0-0.rc2
- Rebuild with new ninja/meson versions, reorganize spec file

* Wed Mar 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.76.0-0.rc1
- Initial spec file for YJL (LFS 11.3)
