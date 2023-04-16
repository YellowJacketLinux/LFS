Name:     cracklib
Version:  2.9.8
Release:  %{?repo}0.rc5%{?dist}
Summary:  A library to somewhat prevent easily crackable passwords

Group:    System Environment/Libraries
License:  LGPLv2.1
URL:      https://github.com/cracklib/cracklib
Source0:  https://github.com/cracklib/cracklib/releases/download/v%{version}/%{name}-%{version}.tar.bz2
Source1:  https://github.com/cracklib/cracklib/releases/download/v%{version}/%{name}-words-%{version}.bz2

Requires: %{name}-common = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  autoconf

%description
CrackLib is a library containing a C function (well, lots of functions
really, but you only need to use one of them) which may be used in a
"passwd"-like program.

The idea is simple: try to prevent users from choosing passwords that
could be guessed by "Crack" by filtering them out, at source.

%package utilities
Summary:  Cracklib utilities
Group:    System Environment/Utilities
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description utilities
This package includes the cracklib utilities

%package common
Summary:  Cracklib common data files
Group:    System Environment/Data
BuildArch:  noarch
Requires(post): %{name}-utilities = %{version}-%{release}

%description common
This package has the common architecture independent files used by
cracklib.

%package devel
Summary:  Developer files for cracklib
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files needed to compile software that
links against the libcrack library.

%package -n python3-cracklib
Summary:  Python bindings for cracklib
Group:    Python/Libraries
Requires: %{name} = %{version}-%{release}
%if %{?python3_ABI:1}%{!?python3_ABI:0}
# Non-Standard Macro
Requires: %{python3_ABI}
%else
Requires: %{python3_sitearch}
%endif

%description -n python3-cracklib
This package contains the Python3 bindings for cracklib.

%prep
%setup -q


%build
autoreconf -fiv
PYTHON=python3
%configure \
  --disable-static \
  --with-default-dict=/usr/lib/cracklib/pw_dict
make %{?_smp_mflags}

%check
make test > %{name}-make.test 2>&1

%install
PYTHON=python3
make install DESTDIR=%{buildroot}
install -m644 -D %{SOURCE1} %{buildroot}%{_datadir}/dict/cracklib-words.bz2
bunzip2 %{buildroot}%{_datadir}/dict/cracklib-words.bz2
touch %{buildroot}%{_datadir}/dict/words
touch %{buildroot}%{_datadir}/dict/cracklib-extra-words
install -m755 -d %{buildroot}/usr/lib/cracklib
touch %{buildroot}/usr/lib/cracklib/pw_dict.hwm
touch %{buildroot}/usr/lib/cracklib/pw_dict.pwd
touch %{buildroot}/usr/lib/cracklib/pw_dict.pwi

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post utilities
if [ ! -L %{_datadir}/dict/words ]; then
  ln -sf cracklib-words %{_datadir}/dict/words
fi
if [ $1 == 1 ]; then
  hname=`hostname`
  [ ! -f %{_datadir}/dict/cracklib-extra-words ] && touch %{_datadir}/dict/cracklib-extra-words
  chmod 644 %{_datadir}/dict/cracklib-extra-words
  echo "$hname" >> %{_datadir}/dict/cracklib-extra-words
fi
if [ -f %{_datadir}/dict/cracklib-extra-words ]; then
  %{_sbindir}/create-cracklib-dict %{_datadir}/dict/words \
                     %{_datadir}/dict/cracklib-extra-words ||:
else
  %{_sbindir}/create-cracklib-dict %{_datadir}/dict/words ||:
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%attr(0755,root,root) %{_libdir}/libcrack.so.2.9.0
%{_libdir}/libcrack.so.2
%license COPYING.LIB
%doc AUTHORS COPYING.LIB NEWS README README-DAWG README-LICENSE README-WORDS
%doc %{name}-make.test

%files utilities
%defattr(-,root,root,-)
%attr(0755,root,root) %{_sbindir}/cracklib-check
%attr(0755,root,root) %{_sbindir}/cracklib-format
%attr(0755,root,root) %{_sbindir}/cracklib-packer
%attr(0755,root,root) %{_sbindir}/cracklib-unpacker
%attr(0755,root,root) %{_sbindir}/create-cracklib-dict

%files common
%defattr(-,root,root,-)
%attr(0755,root,root) %dir /usr/lib/cracklib
%ghost /usr/lib/cracklib/pw_dict.hwm
%ghost /usr/lib/cracklib/pw_dict.pwd
%ghost /usr/lib/cracklib/pw_dict.pwi
%attr(0755,root,root) %dir %{_datadir}/dict
%ghost %{_datadir}/dict/words
%attr(0644,root,root) %{_datadir}/dict/cracklib-words
%ghost %{_datadir}/dict/cracklib-extra-words
%attr(0755,root,root) %dir %{_datadir}/cracklib
%attr(0644,root,root) %{_datadir}/cracklib/cracklib.magic
%attr(0644,root,root) %{_datadir}/cracklib/cracklib-small

%files devel
%defattr(-,root,root,-)
%{_libdir}/libcrack.so
%attr(0644,root,root) %{_includedir}/crack.h
%attr(0644,root,root) %{_includedir}/packer.h

%files -n python3-cracklib
%defattr(-,root,root,-)
%{python3_sitelib}/*.py
%{python3_sitearch}/_cracklib.so
%{python3_sitearch}/__pycache__/*.pyc


%changelog
* Sun Apr 16 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.9.8-0.rc5
- Tabs to spaces, rebuild in newly packaged gcc

* Thu Apr 06 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.9.8-0.rc4
- Properly split off utilities and common subpackages

* Thu Mar 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2.9.8-0.rc3
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
