%global cmakev 3.26

Name:     CMake
Version:  %{cmakev}.3
Release:	%{?repo}0.rc1%{?dist}
Summary:  Tools to build and test software

Group:    Development/Utilities
License:  BSD-3-Clause
URL:      https://cmake.org/
Source0:  https://github.com/Kitware/CMake/releases/download/v%{version}/cmake-%{version}.tar.gz

BuildRequires:  expat-devel
BuildRequires:  gmp-devel
BuildRequires:  libacl-devel
BuildRequires:  libarchive-devel
BuildRequires:  libattr-devel
BuildRequires:  libbz2-devel
BuildRequires:  libcurl-devel
BuildRequires:  libffi-devel
BuildRequires:  libgnutls-devel
BuildRequires:  libhogweed-devel
BuildRequires:  liblzma-devel
BuildRequires:  libnettle-devel
BuildRequires:  libp11-kit-devel
BuildRequires:  libressl-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libtasn1-devel
BuildRequires:  libunistring-devel
BuildRequires:  libuv-devel
BuildRequires:  libxml2-devel
BuildRequires:  libzstd-devel
BuildRequires:  ncurses-devel
BuildRequires:  nghttp2-devel
BuildRequires:  zlib-devel

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
Wed Apr 26 2023 Michael A. Peters <anymouseprophet@gmail.com> - 3.26.3-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
