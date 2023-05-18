%global cmakev 3.26

Name:     cmake
Version:  %{cmakev}.3
Release:	%{?repo}0.rc2%{?dist}
Summary:  Tools to build and test software

Group:    Development/Utilities
License:  BSD-3-Clause
URL:      https://cmake.org/
Source0:  https://github.com/Kitware/CMake/releases/download/v%{version}/cmake-%{version}.tar.gz

BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(gmp)
BuildRequires:  pkgconfig(gmpxx)
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libattr)
BuildRequires:  libbz2-devel
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(hogweed)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(nettle)
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  libressl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(libtasn1)
BuildRequires:  libunistring-devel
BuildRequires:  pkgconfig(libuv)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig(libnghttp2)
BuildRequires:  pkgconfig(zlib)

#Requires:

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files, and generate
native makefiles and workspaces that can be used in the compiler
environment of your choice.


%prep
%setup -n cmake-%{version}
sed -i '/"lib64"/s/64//' Modules/GNUInstallDirs.cmake

%build
./bootstrap --prefix=%{_prefix} \
  --system-libs \
  --mandir=%{_mandir} \
  --no-system-jsoncpp \
  --no-system-librhash 
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_prefix}/doc

mkdir -p rpmdoc/cmlibrhash
cp -p Utilities/cmlibrhash/COPYING rpmdoc/cmlibrhash/
mkdir -p rpmdoc/cmsys
cp -p Source/kwsys/Copyright.txt rpmdoc/cmsys/


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/ccmake
%attr(0755,root,root) %{_bindir}/cmake
%attr(0755,root,root) %{_bindir}/cpack
%attr(0755,root,root) %{_bindir}/ctest
%attr(0644,root,root) %{_datadir}/aclocal/cmake.m4
%attr(0644,root,root) %{_datadir}/bash-completion/completions/cmake
%attr(0644,root,root) %{_datadir}/bash-completion/completions/cpack
%attr(0644,root,root) %{_datadir}/bash-completion/completions/ctest
%{_datadir}/cmake-%{cmakev}
%attr(0644,root,root) %{_datadir}/emacs/site-lisp/cmake-mode.el
%attr(0644,root,root) %{_datadir}/vim/vimfiles/indent/cmake.vim
%attr(0644,root,root) %{_datadir}/vim/vimfiles/syntax/cmake.vim
%license Copyright.txt Licenses 
%doc Copyright.txt rpmdoc/cmlibrhash rpmdoc/cmsys
 
%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.26.3-0.rc2
- Fix package name (CMake -> cmake)
- Fix (some) BuildRequires

* Wed Apr 26 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.26.3-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
