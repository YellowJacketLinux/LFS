%global specrel 0.dev2
%global vimtag 9.0.1459

# Needs work, especially for not 1.core

# Non-English strings *in this spec file* are from Google Translate
#  and may not be as good as they could be.

%global vimwithx 1
%global vimgui gtk3
%global vimfeatures huge
# desktop file support
%global vimdesktopvim 1
%global vimdesktopgvim 1
# the following gets conditionally reset later
%global vimdesktopicons 0
# additional dependencies
%global vimdepgtk3 1

%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global vimwithx 0
%global vimfeatures normal
%global vimdesktopvim 0
%global vimdepgtk3 0
%endif
%if "%{repo}" == "2.cli."
%global vimwithx 0
%global vimdepgtk3 0
%endif
%if "%{repo}" == "5.mate."
%global vimgui gnome2
%endif
%endif

# reset some defaults
%if 0%{vimwithx} == 0
%global vimgui no
%global vimdesktopgvim 0
%endif

%if 0%{vimdesktopvim} == 1
%global vimdesktopicons 1
%endif


Name:     vim
Version:	%{vimtag}
Release:  %{?repo}%{specrel}%{?dist}
Summary:  The vim text editor

Group:		Applications/Text
License:  VIM
URL:      https://www.vim.org/
Source0:  https://github.com/vim/vim/archive/refs/tags/v%{vimtag}.tar.gz
Source1:  etc-vimrc

BuildRequires:  ncurses-devel
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  gpm-devel
%if 0%{vimdepgtk3} == 1
BuildRequires:  gtk3-devel >= 3.24.36
%endif
#Requires:	

%description
Vim is a highly configurable text editor built to make creating and changing any
kind of text very efficient.

%if 0%{vimdesktopvim} == 1
%package desktop
Summary:  VIM Desktop File
Group:    Applications/Text
Requires: vim = %{version}-%{release}
BuildArch:  noarch

%description desktop
This package includes the desktop metadata file needed to add the vim
launcher to the desktop menu.

You only need this package if you want to launch vim from a graphical
desktop menu.
%endif

%if 0%{vimdesktopgvim} == 1
%package -n gvim-desktop
Summary:  Graphical VIM Desktop File
Group:    Applications/Text
Requires: %{_bindir}/gvim
Requires: vim = %{version}-%{release}
BuildArch:  noarch

%description -n gvim-desktop
This package includes the desktop metadata file needed to add the vim
launcher to the desktop menu.

You only need this package if you want to launch vim from a graphical
desktop menu.
%endif



%prep
%setup -q
echo '#define SYS_VIMRC_FILE  "/etc/vimrc"' >>  src/feature.h
echo '#define SYS_GVIMRC_FILE "/etc/gvimrc"' >> src/feature.h


%package man-da
Summary:      vim manual pages in Danish
Summary(da):  vim manual sider på dansk
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-da
This package contains the vim manual pages for the Danish language,
including ISO8859-1 and UTF-8 encodings.

%description(da) man-da
Denne pakke indeholder vim-manualsiderne for det danske sprog, inklusive
ISO8859-1 og UTF-8-kodninger.

%package man-de
Summary:      vim manual pages in German
Summary(de):  vim Handbuchseiten in Deutsch
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-de
This package contains the vim manual pages for the German language,
including ISO8859-1 and UTF-8 encodings.

%description(de) man-de
Dieses Paket enthält die vim-Handbuchseiten für die deutsche Sprache,
einschließlich ISO8859-1- und UTF-8-Kodierungen.

%package man-fr
Summary:      vim manual pages in French
Summary(fr):  vim pages de manuel en français
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-fr
This package contains the vim manual pages for the German language,
including ISO8859-1 and UTF-8 encodings.

%description(fr) man-fr
Ce paquet contient les pages de manuel vim pour la langue allemande,
y compris les encodages ISO8859-1 et UTF-8.

%package man-it
Summary:      vim manual pages in Italian
Summary(it):  vim pagine di manuale in italiano
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-it
This package contains the vim manual pages for the Italian language,
including ISO8859-1 and UTF-8 encodings.

%description(de) man-it
Questo pacchetto contiene le pagine di manuale di vim per la lingua
italiana, comprese le codifiche ISO8859-1 e UTF-8.

%package man-ja
Summary:      vim manual pages in Japanese
Summary(ja):  日本語のvimマニュアルページ
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-ja
This package contains the vim manual pages for the Japanese language.

%description(ja) man-ja
このパッケージには、日本語の vim マニュアル ページが含まれています。

%package man-pl
Summary:      vim manual pages in Polish
Summary(pl):  strony podręcznika vima w języku polskim
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-pl
This package contains the vim manual pages for the Polish language,
including ISO8859-2 and UTF-8 encodings.

%description(pl) man-pl
Ten pakiet zawiera strony podręcznika vima dla języka polskiego, w tym
kodowanie ISO8859-2 i UTF-8.

%package man-ru
Summary:      vim manual pages in Russian
Summary(ru):  справочные страницы vim на русском языке
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-ru
This package contains the vim manual pages for the Russian language,
including KOI8-R and UTF-8 encodings.

%description(ru) man-ru
Этот пакет содержит справочные страницы vim для русского языка, включая
кодировки KOI8-R и UTF-8.

%package man-tr
Summary:      vim manual pages in Turkish
Summary(tr):  Türkçe vim kılavuz sayfaları
Group:        Documentation
Requires:     vim = %{version}-%{release}
BuildArch:    noarch

%description man-tr
This package contains the vim manual pages for the Turkish language,
including ISO8859-9 and UTF-8 encodings.

%description(tr) man-tr
Bu paket, ISO8859-9 ve UTF-8 kodlamaları dahil olmak üzere Türkçe
için vim kılavuz sayfalarını içerir.

%build
%configure \
  --with-features=%{vimfeatures} \
%if 0%{vimwithx} == 0
  --without-x                    \
%else
  --with-gui=%{vimgui}           \
%endif
  --enable-python3interp=dynamic \
  --with-python3=python3         \
  --with-tlib=ncursesw
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
ln -s vim %{buildroot}%{_bindir}/vi

#MAN PAGE SYMLINKS
ln -s vim.1 %{buildroot}%{_mandir}/man1/vi.1
for LANGDIR in da da.ISO8859-1 da.UTF-8 de de.ISO8859-1 de.UTF-8 fr fr.ISO8859-1 fr.UTF-8 it it.ISO8859-1 it.UTF-8 ja pl pl.ISO8859-2 pl.UTF-8 ru.KOI8-R ru.UTF-8 tr tr.ISO8859-9 tr.UTF-8; do
  ln -s vim.1 %{buildroot}%{_mandir}/${LANGDIR}/man1/vi.1
done

install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/vimrc

%if 0%{vimwithx} == 1
sed -i 's?set mouse=$?set mouse=a?' %{buildroot}%{_sysconfdir}/vimrc
%endif

%files
%defattr(-,root,root,-)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/vimrc
%attr(0755,root,root) %{_bindir}/vim
%attr(0755,root,root) %{_bindir}/vimtutor
%attr(0755,root,root) %{_bindir}/xxd
%{_bindir}/ex
%{_bindir}/rview
%{_bindir}/rvim
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/vimdiff
# desktop file support
%if 0%{vimdesktopvim} == 0
%exclude %{_datadir}/applications/vim.desktop
%endif
%if 0%{vimdesktopgvim} == 0
%exclude %{_datadir}/applications/gvim.desktop
%endif
%if 0%{vimdesktopicons} == 0
%exclude %{_datadir}/icons/hicolor/48x48/apps/gvim.png
%exclude %{_datadir}/icons/locolor/16x16/apps/gvim.png
%exclude %{_datadir}/icons/locolor/32x32/apps/gvim.png
%endif
# end desktop file support
%{_datadir}/vim
# man pages
%attr(0644,root,root) %{_mandir}/man1/evim.1*
%attr(0644,root,root) %{_mandir}/man1/vim.1*
%attr(0644,root,root) %{_mandir}/man1/vimdiff.1*
%attr(0644,root,root) %{_mandir}/man1/vimtutor.1*
%attr(0644,root,root) %{_mandir}/man1/xxd.1*
%{_mandir}/man1/ex.1*
%{_mandir}/man1/rview.1*
%{_mandir}/man1/rvim.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%license LICENSE
%doc LICENSE README*

%if 0%{vimdesktopvim} == 1
%files desktop
%defattr(-,root,root,-)
%attr(0644,root,root) %{_datadir}/applications/vim.desktop
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/16x16/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/32x32/apps/gvim.png
%endif

%if 0%{vimdesktopgvim} == 1
%files -n gvim-desktop
%defattr(-,root,root,-)
%attr(0644,root,root) %{_datadir}/applications/vim.desktop
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/16x16/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/32x32/apps/gvim.png
%endif

%files man-da
%defattr(-,root,root,-)
%lang(da) %attr(0644,root,root) %{_mandir}/da/man1/vim.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da/man1/vimdiff.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da/man1/vimtutor.1*
%lang(da) %{_mandir}/da/man1/ex.1*
%lang(da) %{_mandir}/da/man1/rview.1*
%lang(da) %{_mandir}/da/man1/rvim.1*
%lang(da) %{_mandir}/da/man1/vi.1*
%lang(da) %{_mandir}/da/man1/view.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.ISO8859-1/man1/vim.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.ISO8859-1/man1/vimdiff.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.ISO8859-1/man1/vimtutor.1*
%lang(da) %{_mandir}/da.ISO8859-1/man1/ex.1*
%lang(da) %{_mandir}/da.ISO8859-1/man1/rview.1*
%lang(da) %{_mandir}/da.ISO8859-1/man1/rvim.1*
%lang(da) %{_mandir}/da.ISO8859-1/man1/vi.1*
%lang(da) %{_mandir}/da.ISO8859-1/man1/view.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.UTF-8/man1/vim.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.UTF-8/man1/vimdiff.1*
%lang(da) %attr(0644,root,root) %{_mandir}/da.UTF-8/man1/vimtutor.1*
%lang(da) %{_mandir}/da.UTF-8/man1/ex.1*
%lang(da) %{_mandir}/da.UTF-8/man1/rview.1*
%lang(da) %{_mandir}/da.UTF-8/man1/rvim.1*
%lang(da) %{_mandir}/da.UTF-8/man1/vi.1*
%lang(da) %{_mandir}/da.UTF-8/man1/view.1*

%files man-de
%defattr(-,root,root,-)
%lang(de) %attr(0644,root,root) %{_mandir}/de/man1/vim.1*
%lang(de) %{_mandir}/de/man1/ex.1*
%lang(de) %{_mandir}/de/man1/rview.1*
%lang(de) %{_mandir}/de/man1/rvim.1*
%lang(de) %{_mandir}/de/man1/vi.1*
%lang(de) %{_mandir}/de/man1/view.1*
%lang(de) %attr(0644,root,root) %{_mandir}/de.ISO8859-1/man1/vim.1*
%lang(de) %{_mandir}/de.ISO8859-1/man1/ex.1*
%lang(de) %{_mandir}/de.ISO8859-1/man1/rview.1*
%lang(de) %{_mandir}/de.ISO8859-1/man1/rvim.1*
%lang(de) %{_mandir}/de.ISO8859-1/man1/vi.1*
%lang(de) %{_mandir}/de.ISO8859-1/man1/view.1*
%lang(de) %attr(0644,root,root) %{_mandir}/de.UTF-8/man1/vim.1*
%lang(de) %{_mandir}/de.UTF-8/man1/ex.1*
%lang(de) %{_mandir}/de.UTF-8/man1/rview.1*
%lang(de) %{_mandir}/de.UTF-8/man1/rvim.1*
%lang(de) %{_mandir}/de.UTF-8/man1/vi.1*
%lang(de) %{_mandir}/de.UTF-8/man1/view.1*

%files man-fr
%defattr(-,root,root,)
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/evim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/vim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/vimdiff.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/vimtutor.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr/man1/xxd.1*
%lang(fr) %{_mandir}/fr/man1/ex.1*
%lang(fr) %{_mandir}/fr/man1/rview.1*
%lang(fr) %{_mandir}/fr/man1/rvim.1*
%lang(fr) %{_mandir}/fr/man1/vi.1*
%lang(fr) %{_mandir}/fr/man1/view.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.ISO8859-1/man1/evim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.ISO8859-1/man1/vim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.ISO8859-1/man1/vimdiff.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.ISO8859-1/man1/vimtutor.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.ISO8859-1/man1/xxd.1*
%lang(fr) %{_mandir}/fr.ISO8859-1/man1/ex.1*
%lang(fr) %{_mandir}/fr.ISO8859-1/man1/rview.1*
%lang(fr) %{_mandir}/fr.ISO8859-1/man1/rvim.1*
%lang(fr) %{_mandir}/fr.ISO8859-1/man1/vi.1*
%lang(fr) %{_mandir}/fr.ISO8859-1/man1/view.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.UTF-8/man1/evim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.UTF-8/man1/vim.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.UTF-8/man1/vimdiff.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.UTF-8/man1/vimtutor.1*
%lang(fr) %attr(0644,root,root) %{_mandir}/fr.UTF-8/man1/xxd.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/ex.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/rview.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/rvim.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/vi.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/view.1*

%files man-it
%defattr(-,root,root,-)
%lang(it) %attr(0644,root,root) %{_mandir}/it/man1/evim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it/man1/vim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it/man1/vimdiff.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it/man1/vimtutor.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it/man1/xxd.1*
%lang(it) %{_mandir}/it/man1/ex.1*
%lang(it) %{_mandir}/it/man1/rview.1*
%lang(it) %{_mandir}/it/man1/rvim.1*
%lang(it) %{_mandir}/it/man1/vi.1*
%lang(it) %{_mandir}/it/man1/view.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.ISO8859-1/man1/evim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.ISO8859-1/man1/vim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.ISO8859-1/man1/vimdiff.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.ISO8859-1/man1/vimtutor.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.ISO8859-1/man1/xxd.1*
%lang(it) %{_mandir}/it.ISO8859-1/man1/ex.1*
%lang(it) %{_mandir}/it.ISO8859-1/man1/rview.1*
%lang(it) %{_mandir}/it.ISO8859-1/man1/rvim.1*
%lang(it) %{_mandir}/it.ISO8859-1/man1/vi.1*
%lang(it) %{_mandir}/it.ISO8859-1/man1/view.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.UTF-8/man1/evim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.UTF-8/man1/vim.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.UTF-8/man1/vimdiff.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.UTF-8/man1/vimtutor.1*
%lang(it) %attr(0644,root,root) %{_mandir}/it.UTF-8/man1/xxd.1*
%lang(it) %{_mandir}/it.UTF-8/man1/ex.1*
%lang(it) %{_mandir}/it.UTF-8/man1/rview.1*
%lang(it) %{_mandir}/it.UTF-8/man1/rvim.1*
%lang(it) %{_mandir}/it.UTF-8/man1/vi.1*
%lang(it) %{_mandir}/it.UTF-8/man1/view.1*

%files man-ja
%defattr(-,root,root,-)
%lang(ja) %attr(0644,root,root) %{_mandir}/ja/man1/evim.1*
%lang(ja) %attr(0644,root,root) %{_mandir}/ja/man1/vim.1*
%lang(ja) %attr(0644,root,root) %{_mandir}/ja/man1/vimdiff.1*
%lang(ja) %attr(0644,root,root) %{_mandir}/ja/man1/vimtutor.1*
%lang(ja) %attr(0644,root,root) %{_mandir}/ja/man1/xxd.1*
%lang(ja) %{_mandir}/ja/man1/ex.1*
%lang(ja) %{_mandir}/ja/man1/rview.1*
%lang(ja) %{_mandir}/ja/man1/rvim.1*
%lang(ja) %{_mandir}/ja/man1/vi.1*
%lang(ja) %{_mandir}/ja/man1/view.1*

%files man-pl
%defattr(-,root,root,-)
%lang(pl) %attr(0644,root,root) %{_mandir}/pl/man1/evim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl/man1/vim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl/man1/vimdiff.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl/man1/vimtutor.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl/man1/xxd.1*
%lang(pl) %{_mandir}/pl/man1/ex.1*
%lang(pl) %{_mandir}/pl/man1/rview.1*
%lang(pl) %{_mandir}/pl/man1/rvim.1*
%lang(pl) %{_mandir}/pl/man1/vi.1*
%lang(pl) %{_mandir}/pl/man1/view.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.ISO8859-2/man1/evim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.ISO8859-2/man1/vim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.ISO8859-2/man1/vimdiff.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.ISO8859-2/man1/vimtutor.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.ISO8859-2/man1/xxd.1*
%lang(pl) %{_mandir}/pl.ISO8859-2/man1/ex.1*
%lang(pl) %{_mandir}/pl.ISO8859-2/man1/rview.1*
%lang(pl) %{_mandir}/pl.ISO8859-2/man1/rvim.1*
%lang(pl) %{_mandir}/pl.ISO8859-2/man1/vi.1*
%lang(pl) %{_mandir}/pl.ISO8859-2/man1/view.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.UTF-8/man1/evim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.UTF-8/man1/vim.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.UTF-8/man1/vimdiff.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.UTF-8/man1/vimtutor.1*
%lang(pl) %attr(0644,root,root) %{_mandir}/pl.UTF-8/man1/xxd.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/ex.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/rview.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/rvim.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/vi.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/view.1*

%files man-ru
%defattr(-,root,root,-)
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.KOI8-R/man1/evim.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.KOI8-R/man1/vim.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.KOI8-R/man1/vimdiff.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.KOI8-R/man1/vimtutor.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.KOI8-R/man1/xxd.1*
%lang(ru) %{_mandir}/ru.KOI8-R/man1/ex.1*
%lang(ru) %{_mandir}/ru.KOI8-R/man1/rview.1*
%lang(ru) %{_mandir}/ru.KOI8-R/man1/rvim.1*
%lang(ru) %{_mandir}/ru.KOI8-R/man1/vi.1*
%lang(ru) %{_mandir}/ru.KOI8-R/man1/view.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.UTF-8/man1/evim.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.UTF-8/man1/vim.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.UTF-8/man1/vimdiff.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.UTF-8/man1/vimtutor.1*
%lang(ru) %attr(0644,root,root) %{_mandir}/ru.UTF-8/man1/xxd.1*
%lang(ru) %{_mandir}/ru.UTF-8/man1/ex.1*
%lang(ru) %{_mandir}/ru.UTF-8/man1/rview.1*
%lang(ru) %{_mandir}/ru.UTF-8/man1/rvim.1*
%lang(ru) %{_mandir}/ru.UTF-8/man1/vi.1*
%lang(ru) %{_mandir}/ru.UTF-8/man1/view.1*

%files man-tr
%defattr(-,root,root,-)
%lang(tr) %attr(0644,root,root) %{_mandir}/tr/man1/evim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr/man1/vim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr/man1/vimdiff.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr/man1/vimtutor.1*
%lang(tr) %{_mandir}/tr/man1/ex.1*
%lang(tr) %{_mandir}/tr/man1/rview.1*
%lang(tr) %{_mandir}/tr/man1/rvim.1*
%lang(tr) %{_mandir}/tr/man1/vi.1*
%lang(tr) %{_mandir}/tr/man1/view.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.ISO8859-9/man1/evim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.ISO8859-9/man1/vim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.ISO8859-9/man1/vimdiff.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.ISO8859-9/man1/vimtutor.1*
%lang(tr) %{_mandir}/tr.ISO8859-9/man1/ex.1*
%lang(tr) %{_mandir}/tr.ISO8859-9/man1/rview.1*
%lang(tr) %{_mandir}/tr.ISO8859-9/man1/rvim.1*
%lang(tr) %{_mandir}/tr.ISO8859-9/man1/vi.1*
%lang(tr) %{_mandir}/tr.ISO8859-9/man1/view.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.UTF-8/man1/evim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.UTF-8/man1/vim.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.UTF-8/man1/vimdiff.1*
%lang(tr) %attr(0644,root,root) %{_mandir}/tr.UTF-8/man1/vimtutor.1*
%lang(tr) %{_mandir}/tr.UTF-8/man1/ex.1*
%lang(tr) %{_mandir}/tr.UTF-8/man1/rview.1*
%lang(tr) %{_mandir}/tr.UTF-8/man1/rvim.1*
%lang(tr) %{_mandir}/tr.UTF-8/man1/vi.1*
%lang(tr) %{_mandir}/tr.UTF-8/man1/view.1*
# end man pages




%changelog
* Mon Apr 17 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.0.1459-0.dev2
- Split non-English man pages into separate packages, clean up build options.

* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.0.1459-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
