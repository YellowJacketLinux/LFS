%global gitdate 20200201

Name:     msnake
Version:  0.0.%{gitdate}
Release:  %{?rel}0.rc1%{?dist}
Summary:  A curses based snakes game

Group:    Console/Games
License:  MIT
URL:      https://github.com/mogria/msnake
Source0:  %{name}-%{gitdate}.tar.bz2

BuildRequires:  ncurses-devel
BuildRequires:  %{_bindir}/cmake
#Requires:	

%description
A simple snake game written in C using the ncurses library.

%prep
%setup -n %{name}-%{gitdate}


%build
mkdir build
cd build
%{_bindir}/cmake \
   -DCMAKE_INSTALL_PREFIX=/usr \
   ..
make %{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/msnake
%license LICENSE
%doc LICENSE README.md



%changelog
* Fri Apr 28 2023 Michael A. Peters <anymouseprophet@gmail.com> - 0.0.20200201-0.rc1
* Initial spec file
