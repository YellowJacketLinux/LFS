%if 0%{?repo:1} == 1
%if "%{repo}" == "1.core."
%global nofullgui foo
%endif
%endif


Name:     links
Version:  2.29
Release:  %{?repo}0.rc1%{?dist}
Summary:  Console HTTP/2 Web Browser

Group:    Applications/Internet
License:  GPL-2.0-or-later
URL:      http://links.twibright.com/
Source0:  http://links.twibright.com/download/links-%{version}.tar.bz2

BuildRequires:  brotli-devel
BuildRequires:  libbz2-devel
BuildRequires:  libevent-devel
BuildRequires:  liblzma-devel
BuildRequires:  libzstd-devel
BuildRequires:  ncurses-devel
%if 0%{?libresslAPI:1} == 1
BuildRequires:  libressl-devel
%else
BuildRequires:  openssl-devel
%endif
BuildRequires:  GPM-devel
%if 0%{!?nofullgui:1} == 1
BuildRequires:  SVGAlib-devel
BuildRequires:  DirectFB-devel
BuildRequires:  libpng-devel > 1.2.18
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  librsvg-devel
BuildRequires:  libtiff-devel
%endif
#Requires:	

%description
Links is a simple web browser that can run either in a console or in a graphical mode.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/links
%attr(0644,root,root) %{_mandir}/man1/links.1*
%license COPYING
%doc AUTHORS BRAILLE_HOWTO COPYING ChangeLog KEYS NEWS README SITES
%doc Links_logo.png doc/links_cal



%changelog
* Thu Apr 27 2034 Michael A. Peters <anymouseprophet@gmail.com> - 2.29-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
