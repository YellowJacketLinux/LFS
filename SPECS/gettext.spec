%if %{!?insinfo:1}%{?insinfo:0}
%global insinfo /sbin/install-info
%endif

Name:     gettext
Version:  0.21.1
Release:  %{?repo}0.rc1%{?dist}
Summary:  Programs and utilities for multi-lingual messages

Group:    System Environment/Utilities
License:  GPLv3 and LGPLv2.1
URL:      https://www.gnu.org/software/gettext/
Source0:  https://ftp.gnu.org/gnu/gettext/gettext-%{version}.tar.xz

BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libxml2-devel
BuildRequires:  libunistring-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  liblzma-devel
Requires: %{name}-libs = %{version}-%{release}

%description
This package contains the runtime parts of GNU gettext. To create
gettext translations, you will also need the gettext-tools package.

%package libs
Summary:  GNU gettext shared libraries
Group:    System Environment/Libraries
License:  GPLv3 and LGPLv2.1

%description libs
This package contains the shared libraries needed by the GNU gettext
runtime.

%package tools
Summary:  GNU gettext tools
Group:    System Environment/Utilities
License:  GPLv3
Requires: %{name}-libs = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description tools
This package contains the GNU gettext tools that are needed to create
and maintain GNU gettext translations. Most users do not need this
package. Developers and translators will need this package.

%package devel
Summary:  Developer files for libtool
Group:    Development/Libraries
License:  GPLv3 and LGPLv2.1
Requires: %{name} = %{version}-%{release}
Requires: libtextstyle = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description devel
This package contains the files necessary to compile software that
uses the gettext libraries.

%package -n libtextstyle
Summary:  GNU gettext library for producing styled text.
Group:    System Environment/Libraries
License:  GPLv3

%description -n libtextstyle
This library is part of GNU gettext. It can be used to run or develop
programs that produce styled text, to be displayed in a terminal emulator.

%package -n libtextstyle-devel
Summary:  Developer files for libtextstyle
Group:    Development/Libraries
License:  GPLv3
Requires: libtextstyle = %{version}-%{release}
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description -n libtextstyle-devel
This package contains the developer files needed to compile software
that links against the libtextstyle library.

%prep
%setup -q


%build
%configure --disable-static \
  --without-emacs
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log
%else
echo "make check not run during packaging" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
%find_lang gettext-runtime
%find_lang gettext-tools

mkdir rpmdoc
rm -rf %{buildroot}%{_datadir}/doc/libtextstyle
rm -rf %{buildroot}%{_datadir}/doc/libasprintf
mkdir -p rpmdoc/tools/html
cp gettext-tools/man/*.html rpmdoc/tools/html/
cp gettext-tools/doc/*.html rpmdoc/tools/html/
cp -ar gettext-runtime/intl-csharp/doc rpmdoc/csharpdoc
rm -rf %{buildroot}%{_datadir}/doc/gettext

cp gettext-runtime/COPYING gettext-runtime/README-LICENSES
cp gettext-tools/COPYING gettext-tools/README-LICENSE

%post tools
%{insinfo} %{_infodir}/gettext.info %{_infodir}/dir ||:

%preun tools
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gettext.info %{_infodir}/dir ||:
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post devel
%{insinfo} %{_infodir}/autosprintf.info %{_infodir}/dir ||:

%preun devel
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/autosprintf.info %{_infodir}/dir ||:
fi

%post -n libtextstyle -p /sbin/ldconfig
%postun -n libtextstyle -p /sbin/ldconfig

%post -n libtextstyle-devel
%{insinfo} %{_infodir}/libtextstyle.info %{_infodir}/dir ||:

%preun -n libtextstyle
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/libtextstyle.info %{_infodir}/dir ||:
fi


%files -f gettext-runtime.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/envsubst
%attr(0755,root,root) %{_bindir}/gettext
%attr(0755,root,root) %{_bindir}/gettext.sh
%attr(0755,root,root) %{_bindir}/ngettext
%{_datadir}/gettext
%{_datadir}/gettext-%{version}
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/envsubst.1*
%attr(0644,root,root) %{_mandir}/man1/gettext.1*
%attr(0644,root,root) %{_mandir}/man1/ngettext.1*
%license COPYING
%license gettext-runtime/README-LICENSES
%license gettext-runtime/intl/COPYING.LIB
%doc COPYING gettext-runtime/README-LICENSES gettext-runtime/intl/COPYING.LIB
%doc AUTHORS
%doc gettext-runtime/man/*1.html
%doc %{name}-make.check.log

%files tools -f gettext-tools.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/autopoint
%attr(0755,root,root) %{_bindir}/gettextize
%attr(0755,root,root) %{_bindir}/msgattrib
%attr(0755,root,root) %{_bindir}/msgcat
%attr(0755,root,root) %{_bindir}/msgcmp
%attr(0755,root,root) %{_bindir}/msgcomm
%attr(0755,root,root) %{_bindir}/msgconv
%attr(0755,root,root) %{_bindir}/msgen
%attr(0755,root,root) %{_bindir}/msgexec
%attr(0755,root,root) %{_bindir}/msgfilter
%attr(0755,root,root) %{_bindir}/msgfmt
%attr(0755,root,root) %{_bindir}/msggrep
%attr(0755,root,root) %{_bindir}/msginit
%attr(0755,root,root) %{_bindir}/msgmerge
%attr(0755,root,root) %{_bindir}/msgunfmt
%attr(0755,root,root) %{_bindir}/msguniq
%attr(0755,root,root) %{_bindir}/recode-sr-latin
%attr(0755,root,root) %{_bindir}/xgettext
%attr(0755,root,root) %dir %{_libdir}/gettext
%attr(0755,root,root) %{_libdir}/gettext/*
#%%{_datadir}/emacs
%attr(0644,root,root) %{_infodir}/gettext.info*
%attr(0644,root,root) %{_mandir}/man1/autopoint.1*
%attr(0644,root,root) %{_mandir}/man1/gettextize.1*
%attr(0644,root,root) %{_mandir}/man1/msgattrib.1*
%attr(0644,root,root) %{_mandir}/man1/msgcat.1*
%attr(0644,root,root) %{_mandir}/man1/msgcmp.1*
%attr(0644,root,root) %{_mandir}/man1/msgcomm.1*
%attr(0644,root,root) %{_mandir}/man1/msgconv.1*
%attr(0644,root,root) %{_mandir}/man1/msgen.1*
%attr(0644,root,root) %{_mandir}/man1/msgexec.1*
%attr(0644,root,root) %{_mandir}/man1/msgfilter.1*
%attr(0644,root,root) %{_mandir}/man1/msgfmt.1*
%attr(0644,root,root) %{_mandir}/man1/msggrep.1*
%attr(0644,root,root) %{_mandir}/man1/msginit.1*
%attr(0644,root,root) %{_mandir}/man1/msgmerge.1*
%attr(0644,root,root) %{_mandir}/man1/msgunfmt.1*
%attr(0644,root,root) %{_mandir}/man1/msguniq.1*
%attr(0644,root,root) %{_mandir}/man1/recode-sr-latin.1*
%attr(0644,root,root) %{_mandir}/man1/xgettext.1*
%license COPYING
%license gettext-tools/README-LICENSE
%doc AUTHORS COPYING gettext-tools/README-LICENSE
%doc rpmdoc/tools/html gettext-tools/examples

%files libs
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libasprintf.so.0.0.0
%{_libdir}/libasprintf.so.0
%attr(0755,root,root) %{_libdir}/libgettextlib-%{version}.so
%attr(0755,root,root) %{_libdir}/libgettextpo.so.0.5.8
%{_libdir}/libgettextpo.so.0
%attr(0755,root,root) %{_libdir}/libgettextsrc-%{version}.so
%license COPYING
%license gettext-runtime/README-LICENSES
%license gettext-runtime/intl/COPYING.LIB
%doc COPYING gettext-runtime/README-LICENSES gettext-runtime/intl/COPYING.LIB
%doc AUTHORS

%files devel
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/preloadable_libintl.so
%{_libdir}/libasprintf.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextsrc.so
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_datadir}/aclocal/*.m4
%attr(0644,root,root) %{_infodir}/autosprintf.info*
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license COPYING
%license gettext-runtime/README-LICENSES
%license gettext-runtime/intl/COPYING.LIB
%doc COPYING gettext-runtime/README-LICENSES gettext-runtime/intl/COPYING.LIB
%doc AUTHORS
%doc gettext-runtime/libasprintf/autosprintf_all.html
%doc rpmdoc/csharpdoc gettext-runtime/intl-java/javadoc2
%doc gettext-runtime/man/*3.html


%files -n libtextstyle
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libtextstyle.so.0.1.2
%{_libdir}/libtextstyle.so.0
%license libtextstyle/COPYING
%doc libtextstyle/AUTHORS libtextstyle/COPYING

%files -n libtextstyle-devel
%defattr(-,root,root,-)
%{_libdir}/libtextstyle.so
%attr(0755,root,root) %dir %{_includedir}/textstyle
%attr(0644,root,root) %{_includedir}/textstyle/*.h
%attr(0644,root,root) %{_infodir}/libtextstyle.info*
%license libtextstyle/COPYING
%doc libtextstyle/AUTHORS libtextstyle/COPYING
%doc libtextstyle/doc/*.html libtextstyle/examples

%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.21.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
