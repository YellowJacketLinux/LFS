# TODO: docs/Packaging.rst

%global specrel 0.dev3

%if 0%{?!__tar:1} == 1
%global __tar %{_bindir}/tar
%endif
%if 0%{?!__sed:1} == 1
%global __sed %{_bindir}/sed
%endif
%if 0%{?!__ninja:1} == 1
%global __ninja %{_bindir}/ninja
%endif

%if 0%{?repo:1} == 1
%if "%{repo}" == "0.bldsys."
%global nodoxygen nodoxygen
%global novalgrind novalgrind
%endif
%endif

Name:     llvm
Version:  15.0.7
Release:  %{?repo}%{specrel}%{?dist}
Summary:  LLVM (An Optimizing Compiler Infrastructure)

Group:    Development/Tools
License:  Apache-2.0 with exceptions
URL:      https://llvm.org/
Source0:  https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/llvm-%{version}.src.tar.xz
Source1:  https://anduin.linuxfromscratch.org/BLFS/llvm/llvm-cmake-%{version}.src.tar.xz
Source2:  https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/clang-%{version}.src.tar.xz
Source3:  https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/compiler-rt-%{version}.src.tar.xz

#Patch0:   https://www.linuxfromscratch.org/patches/blfs/11.3/clang-15.0.7-enable_default_ssp-1.patch
Patch0:   llvm-clang-15.0.7-enable.patch

BuildRequires:  %{__tar}
BuildRequires:  %{__sed}
BuildRequires:  %{__ninja}
BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  binutils-devel
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  zip
%if 0%{?runtests:1} == 1
BuildRequires:  rsync
%if 0%{?!novalgrind:1} == 1
BuildRequires:  valgrind
BuildRequires:  python3-psutil
%endif
%endif
#Requires:	

%description
The LLVM Project is a collection of modular and reusable compiler and
toolchain technologies. Despite its name, LLVM has little to do with
traditional virtual machines. The name "LLVM" itself is not an acronym;
it is the full name of the project.



%prep
%setup -q -n %{name}-%{version}.src
%__tar -xf %{SOURCE1}
%__sed -i '/LLVM_COMMON_CMAKE_UTILS/s@../cmake@cmake-%{version}.src@' \
  -i CMakeLists.txt

%__tar -xf %{SOURCE2} -C tools
mv tools/clang-%{version}.src tools/clang

%__tar -xf %{SOURCE3} -C projects
mv projects/compiler-rt-%{version}.src projects/compiler-rt

grep -rl '#!.*python' | xargs sed -i '1s/python$/python3/'

%patch 0 -p1

%build
mkdir build && cd build
CC=gcc CXX=g++                                  \
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix}          \
      -DLLVM_ENABLE_FFI=ON                      \
      -DCMAKE_BUILD_TYPE=Release                \
      -DLLVM_BUILD_LLVM_DYLIB=ON                \
      -DLLVM_LINK_LLVM_DYLIB=ON                 \
      -DLLVM_ENABLE_RTTI=ON                     \
      -DLLVM_TARGETS_TO_BUILD="host;AMDGPU;BPF" \
      -DLLVM_BINUTILS_INCDIR=%{_includedir}     \
      -DLLVM_INCLUDE_BENCHMARKS=OFF             \
      -DCLANG_DEFAULT_PIE_ON_LINUX=ON           \
      -Wno-dev -G Ninja ..
%__ninja

%check
cd build
%if 0%{?runtests:1} == 1
%__ninja check-all > %{name}-ninja.check-all.log 2>&1 ||:
%else
echo "ninja check-all not run at package build" > %{name}-ninja.check-all.log
%endif


%install
cd build
DESTDIR=%{buildroot} %__ninja install
install -m755 bin/FileCheck %{buildroot}%{_bindir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_includedir}/clang
%{_includedir}/clang-c
%{_includedir}/llvm
%{_includedir}/llvm-c
# these four are directories
%{_libdir}/clang
%{_libdir}/cmake
%{_libdir}/libear
%{_libdir}/libscanbuild
# end directories
%{_libdir}/libLLVM-15.0.7.so
%{_libdir}/libLLVM.so
%{_libdir}/libLTO.so
%{_libdir}/libRemarks.so
%{_libdir}/libclang-cpp.so
%{_libdir}/libclang.so
%{_libdir}/libclang.so.15
%attr(0755,root,root) %{_libdir}/LLVMgold.so
%attr(0755,root,root) %{_libdir}/libLLVM-15.so
%attr(0755,root,root) %{_libdir}/libLTO.so.15
%attr(0755,root,root) %{_libdir}/libRemarks.so.15
%attr(0755,root,root) %{_libdir}/libclang-cpp.so.15
%attr(0755,root,root) %{_libdir}/libclang.so.15.0.7
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libexecdir}/analyze-c++
%attr(0755,root,root) %{_libexecdir}/analyze-cc
%attr(0755,root,root) %{_libexecdir}/c++-analyzer
%attr(0755,root,root) %{_libexecdir}/ccc-analyzer
%attr(0755,root,root) %{_libexecdir}/intercept-c++
%attr(0755,root,root) %{_libexecdir}/intercept-cc
%dir %{_datadir}/clang
%attr(0755,root,root) %{_datadir}/clang/bash-autocomplete.sh
%attr(0755,root,root) %{_datadir}/clang/clang-format-bbedit.applescript
%attr(0755,root,root) %{_datadir}/clang/clang-format-diff.py
%attr(0755,root,root) %{_datadir}/clang/clang-format-sublime.py
%attr(0755,root,root) %{_datadir}/clang/clang-format.el
%attr(0755,root,root) %{_datadir}/clang/clang-format.py
%attr(0755,root,root) %{_datadir}/clang/clang-rename.el
%attr(0755,root,root) %{_datadir}/clang/clang-rename.py
%dir %{_datadir}/opt-viewer
%attr(0755,root,root) %{_datadir}/opt-viewer/opt-diff.py
%attr(0755,root,root) %{_datadir}/opt-viewer/opt-stats.py
%attr(0755,root,root) %{_datadir}/opt-viewer/opt-viewer.py
%attr(0755,root,root) %{_datadir}/opt-viewer/optpmap.py
%attr(0755,root,root) %{_datadir}/opt-viewer/optrecord.py
%attr(0755,root,root) %{_datadir}/opt-viewer/style.css
%dir %{_datadir}/scan-build
%attr(0644,root,root) %{_datadir}/scan-build/scanview.css
%attr(0644,root,root) %{_datadir}/scan-build/sorttable.js
%dir %{_datadir}/scan-view
%attr(0644,root,root) %{_datadir}/scan-view/Reporter.py
%attr(0644,root,root) %{_datadir}/scan-view/ScanView.py
%attr(0644,root,root) %{_datadir}/scan-view/bugcatcher.ico
%attr(0644,root,root) %{_datadir}/scan-view/startfile.py
%attr(0644,root,root) %{_mandir}/man1/scan-build.1*
%license LICENSE.TXT
%doc CODE_OWNERS.TXT CREDITS.TXT LICENSE.TXT README.txt RELEASE_TESTERS.TXT
%doc docs examples
%doc build/%{name}-ninja.check-all.log



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 15.0.7-0.dev3
- CMake -> cmake in BuildRequires
- Use 0.bldsys. for %%{repo}

* Mon May 15 2023 Michael A. Peters <anymouseprophet@gmail.com> - 15.0.7-0.dev2
- Install FileCheck needed by rustc build

* Sun May 14 2023 Michael A. Peters <anymouseprophet@gmail.com> - 15.0.7-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
