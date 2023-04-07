Name:		gdb
Version:	13.1
Release:	%{?repo}0.rc1%{?dist}
Summary:	GNU Project Debugger

Group:		Development/Utilities
License:	GPLv2 GPLv3 LGPLv2 LGPLv3
URL:		https://www.sourceware.org/gdb/
Source0:	https://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.xz

BuildRequires:	libexpat-devel
BuildRequires:	liblzma-devel
BuildRequires:	libmpfr-devel
#BuildRequires:	libgmp-devel
BuildRequires:	gmp-devel
BuildRequires:	readline-devel
BuildRequires:	libzstd-devel
BuildRequires:	ncurses-devel
BuildRequires:	python3-devel
BuildRequires:	elfutils-devel
BuildRequires:	libstdc++-devel
BuildRequires:	dejagnu
%if %{?python3_ABI:1}%{!?python3_ABI:0}
# Non-Standard Macro
Requires:       %{python3_ABI}
%else
Requires:       %{python3_sitearch}
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what another program
was doing at the moment it crashed.

%prep
%setup -q


%build
mkdir build && cd build
../configure --prefix=%{_prefix} \
  --with-system-readline         \
  --with-python=%{python3}
make %{?_smp_mflags}

# after we have Doxygen
# make -C gdb/doc doxy


%check
cd build/gdb/testsuite
make site.exp
echo  "set gdb_test_timeout 120" >> site.exp
runtest > %{name}-runtest.log 2>&1 ||:


%install
cd build
make -C gdb install DESTDIR=%{buildroot}

# after we have Doxygen
# cp -Rv gdb/doc/doxy /usr/share/doc/gdb-13.1


%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/gcore
%attr(0755,root,root) %{_bindir}/gdb
%attr(0755,root,root) %{_bindir}/gdb-add-index
%attr(0755,root,root) %dir %{_includedir}/gdb
%attr(0644,root,root) %{_includedir}/gdb/jit-reader.h
%{_datadir}/gdb
%attr(0644,root,root) %{_infodir}/annotate.info*
%attr(0644,root,root) %{_infodir}/gdb.info*
%attr(0644,root,root) %{_infodir}/stabs.info*
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_mandir}/man1/gcore.1*
%attr(0644,root,root) %{_mandir}/man1/gdb-add-index.1*
%attr(0644,root,root) %{_mandir}/man1/gdb.1*
%attr(0644,root,root) %{_mandir}/man1/gdbserver.1*
%attr(0644,root,root) %{_mandir}/man5/gdbinit.5*
%license COPYING COPYING.LIB COPYING3 COPYING3.LIB
%doc ChangeLog gdb/README COPYING COPYING.LIB COPYING3 COPYING3.LIB
%doc build/gdb/testsuite/%{name}-runtest.log


%changelog
* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 13.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
