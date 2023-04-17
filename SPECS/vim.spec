# Needs work, especially for none 1.core

%global specrel 0.dev1
%global vimtag 9.0.1459

# buildlevel 0 is slim cli
# buildlevel 1 is additional cli
# buildlevel 2 is basic gui
# buildlevel 3 is mate
%global buildlevel 2
%global vimgui gtk3
%global vimfeatures huge
# desktop file support
%global vimdesktopvim 1
%global vimdesktopgvim 1
%global vimdesktopicons 1

%if %{?repo:1}%{!?repo:0}
%if "%{repo}" == "1.core."
%global buildlevel 0
%global vimgui no
%global vimfeatures normal
%global vimdesktopvim 0
%global vimdesktopgvim 0
%global vimdesktopicons 0
%endif
%if "%{repo}" == "2.cli."
%global buildlevel 1
%global vimgui no
%global vimdesktopgvim 0
%endif
%if "%{repo}" == "5.mate."
%global buildlevel 3
%global vimgui gnome2
%endif
%endif


Name:     vim
Version:	%{vimtag}
Release:  %{?repo}%{specrel}%{?dist}
Summary:  The vim text editor

Group:		Applications/Text
License:  VIM
URL:      https://www.vim.org/
Source0:	https://github.com/vim/vim/archive/refs/tags/v%{vimtag}.tar.gz
Source1:  etc-vimrc

BuildRequires:  ncurses-devel
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  gpm-devel
%if 0%{buildlevel} > 1
BuildRequires:  gtk+-devel >= 3.24.36
%endif
#Requires:	

%description
Vim is a highly configurable text editor built to make creating and changing any
kind of text very efficient.

%prep
%setup -q
echo '#define SYS_VIMRC_FILE  "/etc/vimrc"' >>  src/feature.h
%if 0%{buildlevel} == 1
echo '#define SYS_GVIMRC_FILE "/etc/gvimrc"' >> src/feature.h
%endif



%build
%configure \
  --with-features=%{vimfeatures} \
%if 0%{buildlevel} < 2
  --without-x                    \
%else
  --with-gui=%{vimgui}           \
%endif
%if 0%{buildlevel} > 0
  --enable-python3interp=dynamic \
  --with-python3=python3         \
%endif
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
%if 0%{vimdesktopvim} == 1
%attr(0644,root,root) %{_datadir}/applications/vim.desktop
%else
%exclude %{_datadir}/applications/vim.desktop
%endif
%if 0%{vimdesktopgvim} == 1
%attr(0644,root,root) %{_datadir}/applications/gvim.desktop
%else
%exclude %{_datadir}/applications/gvim.desktop
%endif
%if 0%{vimdesktopicons} == 1
%attr(0644,root,root) %{_datadir}/icons/hicolor/48x48/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/16x16/apps/gvim.png
%attr(0644,root,root) %{_datadir}/icons/locolor/32x32/apps/gvim.png
%else
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
# %%lang(da)
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
# %%lang(de)
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
# %%lang(fr)
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
# %%lang(it)
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
# %%lang(ja)
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
# %%lang(pl)
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
# %%lang(ru)
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
# %%lang(tr)
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
%license LICENSE
%doc LICENSE README*



%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 9.0.1459-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
