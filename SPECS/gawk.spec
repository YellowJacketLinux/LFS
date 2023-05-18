%if 0%{?!insinfo:1} == 1
%global insinfo /sbin/install-info
%endif

Name:     gawk
Version:  5.2.1
Release:  %{?repo}0.rc2%{?dist}
Summary:  GNU Awk

Group:    Development/Utilities
License:  GPLv3
URL:      https://www.gnu.org/software/gawk/
Source0:  https://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz

#BuildRequires:	
Requires(post):   %{insinfo}
Requires(preun):  %{insinfo}

%description
If you are like many computer users, you would frequently like to make
changes in various text files wherever certain patterns appear, or
extract data from parts of certain lines while discarding the rest. To
write a program to do this in a language such as C or Pascal is a time-
consuming inconvenience that may take many lines of code. The job is
easy with awk, especially the GNU implementation: gawk.


%prep
%setup -q
sed -i 's/extras//' Makefile.in


%build
%configure
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
make check > %{name}-make.check.log 2>&1
%else
echo "make check not run during package build" > %{name}-make.check.log
%endif

%install
make install DESTDIR=%{buildroot}
%find_lang gawk

%post
%{insinfo} %{_infodir}/gawk.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gawkinet.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/gawkworkflow.info %{_infodir}/dir ||:
%{insinfo} %{_infodir}/pm-gawk.info %{_infodir}/dir ||:

%preun
if [ $1 = 0 ]; then
%{insinfo} --delete %{_infodir}/gawk.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gawkinet.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/gawkworkflow.info %{_infodir}/dir ||:
%{insinfo} --delete %{_infodir}/pm-gawk.info %{_infodir}/dir ||:
fi

%files -f gawk.lang
%defattr(-,root,root,-)
%{_bindir}/awk
%attr(0755,root,root) %{_bindir}/gawk
%attr(0755,root,root) %{_bindir}/gawk-%{version}
%attr(0755,root,root) %{_bindir}/gawkbug
%attr(0644,root,root) %{_includedir}/gawkapi.h
%attr(0755,root,root) %dir %{_libdir}/gawk
%attr(0755,root,root) %{_libdir}/gawk/*.so
%attr(0755,root,root) %dir %{_libexecdir}/awk
%attr(0755,root,root) %{_libexecdir}/awk/grcat
%attr(0755,root,root) %{_libexecdir}/awk/pwcat
%attr(0755,root,root) %dir %{_datadir}/awk
%attr(0644,root,root) %{_datadir}/awk/*.awk
%exclude %{_infodir}/dir
%attr(0644,root,root) %{_infodir}/gawk.info*
%attr(0644,root,root) %{_infodir}/gawkinet.info*
%attr(0644,root,root) %{_infodir}/gawkworkflow.info*
%attr(0644,root,root) %{_infodir}/pm-gawk.info*
%attr(0644,root,root) %{_mandir}/man1/*.1*
%attr(0644,root,root) %{_mandir}/man3/*.3*
%license COPYING
%doc AUTHORS ChangeLog* COPYING NEWS* README TODO gawk-make.check.log
%doc doc/awkforai.txt doc/*.eps doc/*.pdf doc/*.jpg doc/*.png



%changelog
* Thu May 18 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.1-0.rc2
- Minor spec file cleanup

* Mon Apr 10 2023 Michael A. Peters <anymouseprophet@gmail.com> - 5.2.1-0.rc1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
