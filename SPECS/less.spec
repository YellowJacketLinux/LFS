Name:     less
Version:  608
Release:	1%{?dist}
Summary:  Pager for displaying text files

Group:    System Environment/Utilities
License:  GPLv3 and Less License
URL:      https://www.greenwoodsoftware.com/less/
Source0:  https://www.greenwoodsoftware.com/less/less-%{version}.tar.gz

BuildRequires:  ncurses-devel
#Requires:

%description
Less is a free, open-source file pager. It can be found on most versions
of Linux, Unix and Mac OS, as well as on many other operating systems.

Less is a replacement for the traditional Unix pager program 'more' so
it can be said that 'less is more, more or less...'

It should be noted that 'less' has more capabilities than the traditional
Unix pager 'more' and thus it is frequently installed on those systems
as well as being the standard file pager on newer "Unix-Like but not
really Unix" systems such as GNU/Linux.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/less
%attr(0755,root,root) %{_bindir}/lessecho
%attr(0755,root,root) %{_bindir}/lesskey
%attr(0644,root,root) %{_mandir}/man1/less.1*
%attr(0644,root,root) %{_mandir}/man1/lessecho.1*
%attr(0644,root,root) %{_mandir}/man1/lesskey.1*
%license COPYING LICENSE README
%doc COPYING LICENSE NEWS README

%changelog
* Tue Apr 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 608-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
