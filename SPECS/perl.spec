%global specrel 0.dev2

### UNFINISHED ###
#
# As of 0.dev1 (Thu Apr 20 2023) this spec file just builds one big
#  package that contains everything.
#
# Before it hits rc1 it will be split into numerous sub-packages
#  so that users don't need to install the parts they do not need
#  and so that a bug fix that involves just a file or two doesn't
#  mean a massive RPM update.
#

%global __requires_exclude ^perl\\((Mac|VMS|unicore)

# Version definitions
%global perl5_version 5.36

# General macros
%global __perl /usr/bin/perl
%global perl5 %__perl
%global perl5_privlib    %{_prefix}/lib/perl5/%{perl5_version}/core_perl
%global perl5_archlib    %{_libdir}/perl5/%{perl5_version}/core_perl
%global perl5_sitelib    %{_prefix}/lib/perl5/%{perl5_version}/site_perl
%global perl5_sitearch   %{_libdir}/perl5/%{perl5_version}/site_perl
%global perl5_vendorlib  %{_prefix}/lib/perl5/%{perl5_version}/vendor_perl
%global perl5_vendorarch %{_libdir}/perl5/%{perl5_version}/vendor_perl

%if "%{_lib}" == "lib64"
%global linuxMultiarch true
%endif

Name:     perl
# Seems that Fedora/RHEL are at epoch 4 ????
#  Epoch 2 seems to be at least needed because of
#  internal perl requires
Epoch:    2
Version:  %{perl5_version}.0
Release:  %{?repo}%{specrel}%{?dist}
Summary:  People Hate Perl

Group:    Programming/Languages
License:  GPL or Perl Artistic
URL:      https://www.perl.org/
Source0:  https://www.cpan.org/src/5.0/perl-%{version}.tar.xz
Source1:  rpm-macros-perl-5.36

#BuildRequires:	
#Requires:	

%description
Perl is a highly capable, feature-rich programming language with over
30 years of development. Perl runs on over 100 platforms from portables
to mainframes and is suitable for both rapid prototyping and large scale
development projects.

%prep
%setup -q


%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0

sh Configure -des                   \
  -Dprefix=%{_prefix}               \
  -Dvendorprefix=%{_prefix}         \
  -Dprivlib=%{perl5_privlib}        \
  -Darchlib=%{perl5_archlib}        \
  -Dsitelib=%{perl5_sitelib}        \
  -Dsitearch=%{perl5_sitearch}      \
  -Dvendorlib=%{perl5_vendorlib}    \
  -Dvendorarch=%{perl5_vendorarch}  \
  -Dman1dir=%{_mandir}/man1         \
  -Dman3dir=%{_mandir}/man3         \
  -Dpager="%{_bindir}/less -isR"    \
  -Duseshrplib                      \
  -Dusethreads
           
make %{?_smp_mflags}

%check
%if 0%{?runtests:1} == 1
export PERL_BUILD_PACKAGING=foo
export CI=true
export BUILD_ZLIB=False
export BUILD_BZIP2=0
echo "Running make test. This will take awhile."
make test > %{name}-make.test.log 2>&1
%else
echo "make check not run during packaging" > %{name}-make.test.log
%endif

%install
export BUILD_ZLIB=False
export BUILD_BZIP2=0
make install DESTDIR=%{buildroot}
[ ! -d %{buildroot}%{perl5_sitearch}/auto ] && \
  mkdir -p %{buildroot}%{perl5_sitearch}/auto
[ ! -d %{buildroot}%{perl5_sitelib} ] && \
  mkdir -p %{buildroot}%{perl5_sitelib}
[ ! -d %{buildroot}%{perl5_vendorarch}/auto ] && \
  mkdir -p %{buildroot}%{perl5_vendorarch}/auto
[ ! -d %{buildroot}%{perl5_vendorlib} ] && \
  mkdir -p %{buildroot}%{perl5_vendorlib}

install -m755 -d %{buildroot}/usr/lib/rpm/macros.d
install -m644 %{SOURCE1} %{buildroot}/usr/lib/rpm/macros.d/macros.perl

##
## /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w
%{_fixperms} %{buildroot}%{perl5_archlib}
%if 0%{?linuxMultiarch:1} == 1
%{_fixperms} %{buildroot}%{perl5_privlib}
%endif


%files
%defattr(-,root,root,-)
###
# rpm macro file
###
%attr(0644,root,root) /usr/lib/rpm/macros.d/macros.perl
###
# /usr/bin stuff
###
%attr(0755,root,root) %{_bindir}/corelist
%attr(0755,root,root) %{_bindir}/cpan
%attr(0755,root,root) %{_bindir}/enc2xs
%attr(0755,root,root) %{_bindir}/encguess
%attr(0755,root,root) %{_bindir}/h2ph
%attr(0755,root,root) %{_bindir}/h2xs
%attr(0755,root,root) %{_bindir}/instmodsh
%attr(0755,root,root) %{_bindir}/json_pp
%attr(0755,root,root) %{_bindir}/libnetcfg
%attr(0755,root,root) %{_bindir}/perl
%attr(0755,root,root) %{_bindir}/perl5.36.0
%attr(0755,root,root) %{_bindir}/perlbug
%attr(0755,root,root) %{_bindir}/perldoc
%attr(0755,root,root) %{_bindir}/perlivp
%attr(0755,root,root) %{_bindir}/perlthanks
%attr(0755,root,root) %{_bindir}/piconv
%attr(0755,root,root) %{_bindir}/pl2pm
%attr(0755,root,root) %{_bindir}/pod2html
%attr(0755,root,root) %{_bindir}/pod2man
%attr(0755,root,root) %{_bindir}/pod2text
%attr(0755,root,root) %{_bindir}/pod2usage
%attr(0755,root,root) %{_bindir}/podchecker
%attr(0755,root,root) %{_bindir}/prove
%attr(0755,root,root) %{_bindir}/ptar
%attr(0755,root,root) %{_bindir}/ptardiff
%attr(0755,root,root) %{_bindir}/ptargrep
%attr(0755,root,root) %{_bindir}/shasum
%attr(0755,root,root) %{_bindir}/splain
%attr(0755,root,root) %{_bindir}/streamzip
%attr(0755,root,root) %{_bindir}/xsubpp
%attr(0755,root,root) %{_bindir}/zipdetails
###
# /usr/lib/perl stuff
###
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{perl5_version}
%dir %{_libdir}/perl5/%{perl5_version}/core_perl
%dir %{_libdir}/perl5/%{perl5_version}/core_perl/auto
%dir %{_libdir}/perl5/%{perl5_version}/site_perl
%dir %{_libdir}/perl5/%{perl5_version}/site_perl/auto
%dir %{_libdir}/perl5/%{perl5_version}/vendor_perl
%dir %{_libdir}/perl5/%{perl5_version}/vendor_perl/auto
%if 0%{?linuxMultiarch:1} == 1
%dir %{_prefix}/lib/perl5
%dir %{_prefix}/lib/perl5/%{perl5_version}
%dir %{_prefix}/lib/perl5/%{perl5_version}/core_perl
%dir %{_prefix}/lib/perl5/%{perl5_version}/site_perl
%dir %{_prefix}/lib/perl5/%{perl5_version}/vendor_perl
%endif
###
# AnyDBM_File.pm
%attr(0444,root,root) %{perl5_privlib}/AnyDBM_File.pm
# App
%dir %{perl5_privlib}/App
%attr(0444,root,root) %{perl5_privlib}/App/Cpan.pm
%attr(0444,root,root) %{perl5_privlib}/App/Prove.pm
%dir %{perl5_privlib}/App/Prove
%attr(0444,root,root) %{perl5_privlib}/App/Prove/State.pm
%dir %{perl5_privlib}/App/Prove/State/
%attr(0444,root,root) %{perl5_privlib}/App/Prove/State/Result.pm
%dir %{perl5_privlib}/App/Prove/State/Result
%attr(0444,root,root) %{perl5_privlib}/App/Prove/State/Result/Test.pm
# Archive
%dir %{perl5_privlib}/Archive
%attr(0444,root,root) %{perl5_privlib}/Archive/Tar.pm
%dir %{perl5_privlib}/Archive/Tar
%attr(0444,root,root) %{perl5_privlib}/Archive/Tar/Constant.pm
%attr(0444,root,root) %{perl5_privlib}/Archive/Tar/File.pm
# Attribute
%dir %{perl5_privlib}/Attribute
%attr(0444,root,root) %{perl5_privlib}/Attribute/Handlers.pm
# AutoLoader.pm -- AutoSplit.pm
%attr(0444,root,root) %{perl5_privlib}/AutoLoader.pm
%attr(0444,root,root) %{perl5_privlib}/AutoSplit.pm
#B
%attr(0444,root,root) %{perl5_archlib}/B.pm
%dir %{perl5_archlib}/B
%attr(0444,root,root) %{perl5_archlib}/B/Concise.pm
%attr(0444,root,root) %{perl5_archlib}/B/Showlex.pm
%attr(0444,root,root) %{perl5_archlib}/B/Terse.pm
%attr(0444,root,root) %{perl5_archlib}/B/Xref.pm
%dir %{perl5_archlib}/auto/B
%attr(0555,root,root) %{perl5_archlib}/auto/B/*.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/B
%endif
%attr(0444,root,root) %{perl5_privlib}/B/Deparse.pm
%attr(0444,root,root) %{perl5_privlib}/B/Op_private.pm
# Benchmark.pm
%attr(0444,root,root) %{perl5_privlib}/Benchmark.pm
#CORE
%dir %{perl5_archlib}/CORE
%attr(0444,root,root) %{perl5_archlib}/CORE/*.h
%attr(0555,root,root) %{perl5_archlib}/CORE/libperl.so
%attr(0444,root,root) %{perl5_privlib}/CORE.pod
# CPAN
%attr(0444,root,root) %{perl5_privlib}/CPAN.pm
%dir %{perl5_privlib}/CPAN
%dir %{perl5_privlib}/CPAN/API
%attr(0444,root,root) %{perl5_privlib}/CPAN/API/HOWTO.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Author.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Bundle.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/CacheMgr.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Complete.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Debug.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/DeferredCode.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Distribution.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Distroprefs.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Distrostatus.pm
%dir %{perl5_privlib}/CPAN/Exception
%attr(0444,root,root) %{perl5_privlib}/CPAN/Exception/RecursiveDependency.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Exception/blocked_urllist.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Exception/yaml_not_installed.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Exception/yaml_process_error.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/FTP.pm
%dir %{perl5_privlib}/CPAN/FTP
%attr(0444,root,root) %{perl5_privlib}/CPAN/FTP/netrc.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/FirstTime.pm
%dir %{perl5_privlib}/CPAN/HTTP
%attr(0444,root,root) %{perl5_privlib}/CPAN/HTTP/Client.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/HTTP/Credentials.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/HandleConfig.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Index.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/InfoObj.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Kwalify.pm
%dir %{perl5_privlib}/CPAN/Kwalify
%attr(0444,root,root) %{perl5_privlib}/CPAN/Kwalify/distroprefs.dd
%attr(0444,root,root) %{perl5_privlib}/CPAN/Kwalify/distroprefs.yml
%dir %{perl5_privlib}/CPAN/LWP
%attr(0444,root,root) %{perl5_privlib}/CPAN/LWP/UserAgent.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta.pm
%dir %{perl5_privlib}/CPAN/Meta
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Converter.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Feature.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History.pm
%dir %{perl5_privlib}/CPAN/Meta/History
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History/Meta_1_0.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History/Meta_1_1.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History/Meta_1_2.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History/Meta_1_3.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/History/Meta_1_4.pod
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Merge.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Prereqs.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Requirements.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Spec.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/Validator.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Meta/YAML.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Mirrors.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Module.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Nox.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Plugin.pm
%dir %{perl5_privlib}/CPAN/Plugin
%attr(0444,root,root) %{perl5_privlib}/CPAN/Plugin/Specfile.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Prompt.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Queue.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Shell.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Tarzip.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/URL.pm
%attr(0444,root,root) %{perl5_privlib}/CPAN/Version.pm
# Carp
%attr(0444,root,root) %{perl5_privlib}/Carp.pm
%dir %{perl5_privlib}/Carp
%attr(0444,root,root) %{perl5_privlib}/Carp/Heavy.pm
# Class
%dir %{perl5_privlib}/Class
%attr(0444,root,root) %{perl5_privlib}/Class/Struct.pm
#Compress
%dir %{perl5_archlib}/Compress
%dir %{perl5_archlib}/Compress/Raw
%attr(0444,root,root) %{perl5_archlib}/Compress/Raw/Bzip2.pm
%attr(0444,root,root) %{perl5_archlib}/Compress/Raw/Zlib.pm
%dir %{perl5_archlib}/auto/Compress
%dir %{perl5_archlib}/auto/Compress/Raw
%dir %{perl5_archlib}/auto/Compress/Raw/Bzip2
%attr(0555,root,root) %{perl5_archlib}/auto/Compress/Raw/Bzip2/Bzip2.so
%dir %{perl5_archlib}/auto/Compress/Raw/Zlib
%attr(0555,root,root) %{perl5_archlib}/auto/Compress/Raw/Zlib/Zlib.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Compress
%endif
%attr(0444,root,root) %{perl5_privlib}/Compress/Zlib.pm
#Config
%attr(0444,root,root) %{perl5_archlib}/Config.pm
%attr(0444,root,root) %{perl5_archlib}/Config.pod
%attr(0444,root,root) %{perl5_archlib}/Config_git.pl
%attr(0444,root,root) %{perl5_archlib}/Config_heavy.pl
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Config
%endif
%attr(0444,root,root) %{perl5_privlib}/Config/Extensions.pm
%dir %{perl5_privlib}/Config/Perl
%attr(0444,root,root) %{perl5_privlib}/Config/Perl/V.pm
#Cwd
%attr(0444,root,root) %{perl5_archlib}/Cwd.pm
%dir %{perl5_archlib}/auto/Cwd
%attr(0555,root,root) %{perl5_archlib}/auto/Cwd/Cwd.so
# DB.pm
%attr(0444,root,root) %{perl5_privlib}/DB.pm
# DBM_Filter
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter.pm
%dir %{perl5_privlib}/DBM_Filter
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter/compress.pm
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter/encode.pm
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter/int32.pm
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter/null.pm
%attr(0444,root,root) %{perl5_privlib}/DBM_Filter/utf8.pm
#Data
%dir %{perl5_archlib}/Data
%attr(0444,root,root) %{perl5_archlib}/Data/Dumper.pm
%dir %{perl5_archlib}/auto/Data
%dir %{perl5_archlib}/auto/Data/Dumper
%attr(0555,root,root) %{perl5_archlib}/auto/Data/Dumper/Dumper.so
#Devel
%dir %{perl5_archlib}/Devel
%attr(0444,root,root) %{perl5_archlib}/Devel/PPPort.pm
%attr(0444,root,root) %{perl5_archlib}/Devel/Peek.pm
%dir %{perl5_archlib}/auto/Devel
%dir %{perl5_archlib}/auto/Devel/Peek
%attr(0555,root,root) %{perl5_archlib}/auto/Devel/Peek/Peek.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Devel
%endif
%attr(0444,root,root) %{perl5_privlib}/Devel/SelfStubber.pm
# Digest
%dir %{perl5_archlib}/Digest
%attr(0444,root,root) %{perl5_archlib}/Digest/MD5.pm
%attr(0444,root,root) %{perl5_archlib}/Digest/SHA.pm
%dir %{perl5_archlib}/auto/Digest
%dir %{perl5_archlib}/auto/Digest/MD5
%attr(0555,root,root) %{perl5_archlib}/auto/Digest/MD5/MD5.so
%dir %{perl5_archlib}/auto/Digest/SHA
%attr(0555,root,root) %{perl5_archlib}/auto/Digest/SHA/SHA.so
%attr(0444,root,root) %{perl5_privlib}/Digest.pm
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Digest
%endif
%attr(0444,root,root) %{perl5_privlib}/Digest/base.pm
%attr(0444,root,root) %{perl5_privlib}/Digest/file.pm
# DirHandle.pm -- Dumpvalue.pm
%attr(0444,root,root) %{perl5_privlib}/DirHandle.pm
%attr(0444,root,root) %{perl5_privlib}/Dumpvalue.pm
#DynaLoader
%attr(0444,root,root) %{perl5_archlib}/DynaLoader.pm
#Encode
%attr(0444,root,root) %{perl5_archlib}/Encode.pm
%dir %{perl5_archlib}/Encode
%attr(0444,root,root) %{perl5_archlib}/Encode/Alias.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Byte.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/CJKConstants.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/CN.pm
%dir %{perl5_archlib}/Encode/CN
%attr(0444,root,root) %{perl5_archlib}/Encode/CN/HZ.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Config.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/EBCDIC.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Encoder.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Encoding.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/GSM0338.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Guess.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/JP.pm
%dir %{perl5_archlib}/Encode/JP
%attr(0444,root,root) %{perl5_archlib}/Encode/JP/H2Z.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/JP/JIS7.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/KR.pm
%dir %{perl5_archlib}/Encode/KR
%attr(0444,root,root) %{perl5_archlib}/Encode/KR/2022_KR.pm
%dir %{perl5_archlib}/Encode/MIME
%attr(0444,root,root) %{perl5_archlib}/Encode/MIME/Header.pm
%dir %{perl5_archlib}/Encode/MIME/Header
%attr(0444,root,root) %{perl5_archlib}/Encode/MIME/Header/ISO_2022_JP.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/MIME/Name.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Symbol.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/TW.pm
%attr(0444,root,root) %{perl5_archlib}/Encode/Unicode.pm
%dir %{perl5_archlib}/Encode/Unicode
%attr(0444,root,root) %{perl5_archlib}/Encode/Unicode/UTF7.pm
%dir %{perl5_archlib}/auto/Encode
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/Encode.so
%dir %{perl5_archlib}/auto/Encode/Byte
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/Byte/Byte.so
%dir %{perl5_archlib}/auto/Encode/CN
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/CN/CN.so
%dir %{perl5_archlib}/auto/Encode/EBCDIC
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/EBCDIC/EBCDIC.so
%dir %{perl5_archlib}/auto/Encode/JP
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/JP/JP.so
%dir %{perl5_archlib}/auto/Encode/KR
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/KR/KR.so
%dir %{perl5_archlib}/auto/Encode/Symbol
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/Symbol/Symbol.so
%dir %{perl5_archlib}/auto/Encode/TW
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/TW/TW.so
%dir %{perl5_archlib}/auto/Encode/Unicode
%attr(0555,root,root) %{perl5_archlib}/auto/Encode/Unicode/Unicode.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Encode
%endif
%attr(0444,root,root) %{perl5_privlib}/Encode/Changes.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/ConfigLocal_PM.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/Makefile_PL.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/PerlIO.pod
%attr(0444,root,root) %{perl5_privlib}/Encode/README.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/Supported.pod
%attr(0444,root,root) %{perl5_privlib}/Encode/_PM.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/_T.e2x
%attr(0444,root,root) %{perl5_privlib}/Encode/encode.h
# English.pm -- Env.pm
%attr(0444,root,root) %{perl5_privlib}/English.pm
%attr(0444,root,root) %{perl5_privlib}/Env.pm
# Errno
%attr(0444,root,root) %{perl5_archlib}/Errno.pm
# Exporter
%attr(0444,root,root) %{perl5_privlib}/Exporter.pm
%dir %{perl5_privlib}/Exporter
%attr(0444,root,root) %{perl5_privlib}/Exporter/Heavy.pm
# ExtUtils
%dir %{perl5_privlib}/ExtUtils
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder.pm
%dir %{perl5_privlib}/ExtUtils/CBuilder
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Base.pm
%dir %{perl5_privlib}/ExtUtils/CBuilder/Platform
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/Unix.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/VMS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/Windows.pm
%dir %{perl5_privlib}/ExtUtils/CBuilder/Platform/Windows
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/Windows/BCC.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/Windows/GCC.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/Windows/MSVC.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/aix.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/android.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/cygwin.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/darwin.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/dec_osf.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/CBuilder/Platform/os2.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Command.pm
%dir %{perl5_privlib}/ExtUtils/Command
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Command/MM.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Constant.pm
%dir %{perl5_privlib}/ExtUtils/Constant
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Constant/Base.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Constant/ProxySubs.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Constant/Utils.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Constant/XS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Embed.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Install.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Installed.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Liblist.pm
%dir %{perl5_privlib}/ExtUtils/Liblist
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Liblist/Kid.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MANIFEST.SKIP
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_AIX.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Any.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_BeOS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Cygwin.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_DOS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Darwin.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_MacOS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_NW5.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_OS2.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_OS390.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_QNX.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_UWIN.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Unix.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_VMS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_VOS.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Win32.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MM_Win95.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MY.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker.pm
%dir %{perl5_privlib}/ExtUtils/MakeMaker
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker/Config.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker/FAQ.pod
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker/Locale.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker/Tutorial.pod
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/MakeMaker/version.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Manifest.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Miniperl.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Mkbootstrap.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Mksymlists.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/PL2Bat.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Packlist.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS.pm
%dir %{perl5_privlib}/ExtUtils/ParseXS
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS/Constants.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS/CountLines.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS/Eval.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS/Utilities.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/ParseXS.pod
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Typemaps.pm
%dir %{perl5_privlib}/ExtUtils/Typemaps
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Typemaps/Cmd.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Typemaps/InputMap.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Typemaps/OutputMap.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/Typemaps/Type.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/testlib.pm
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/typemap
%attr(0444,root,root) %{perl5_privlib}/ExtUtils/xsubpp
# Fatal.pm
%attr(0444,root,root) %{perl5_privlib}/Fatal.pm
# Fcntl
%attr(0444,root,root) %{perl5_archlib}/Fcntl.pm
%dir %{perl5_archlib}/auto/Fcntl
%attr(0555,root,root) %{perl5_archlib}/auto/Fcntl/Fcntl.so
# File
%dir %{perl5_archlib}/File
%attr(0444,root,root) %{perl5_archlib}/File/DosGlob.pm
%attr(0444,root,root) %{perl5_archlib}/File/Glob.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec.pm
%dir %{perl5_archlib}/File/Spec
%attr(0444,root,root) %{perl5_archlib}/File/Spec/AmigaOS.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Cygwin.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Epoc.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Functions.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Mac.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/OS2.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Unix.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/VMS.pm
%attr(0444,root,root) %{perl5_archlib}/File/Spec/Win32.pm
%dir %{perl5_archlib}/auto/File
%dir %{perl5_archlib}/auto/File/DosGlob
%attr(0555,root,root) %{perl5_archlib}/auto/File/DosGlob/DosGlob.so
%dir %{perl5_archlib}/auto/File/Glob
%attr(0555,root,root) %{perl5_archlib}/auto/File/Glob/Glob.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/File
%endif
%attr(0444,root,root) %{perl5_privlib}/File/Basename.pm
%attr(0444,root,root) %{perl5_privlib}/File/Compare.pm
%attr(0444,root,root) %{perl5_privlib}/File/Copy.pm
%attr(0444,root,root) %{perl5_privlib}/File/Fetch.pm
%attr(0444,root,root) %{perl5_privlib}/File/Find.pm
%attr(0444,root,root) %{perl5_privlib}/File/GlobMapper.pm
%attr(0444,root,root) %{perl5_privlib}/File/Path.pm
%attr(0444,root,root) %{perl5_privlib}/File/Temp.pm
%attr(0444,root,root) %{perl5_privlib}/File/stat.pm
# FileCache.pm -- FileHandle.pm
%attr(0444,root,root) %{perl5_privlib}/FileCache.pm
%attr(0444,root,root) %{perl5_privlib}/FileHandle.pm
# Filter
%dir %{perl5_archlib}/Filter
%dir %{perl5_archlib}/Filter/Util
%attr(0444,root,root) %{perl5_archlib}/Filter/Util/Call.pm
%dir %{perl5_archlib}/auto/Filter
%dir %{perl5_archlib}/auto/Filter/Util
%dir %{perl5_archlib}/auto/Filter/Util/Call
%attr(0555,root,root) %{perl5_archlib}/auto/Filter/Util/Call/Call.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Filter
%endif
%attr(0444,root,root) %{perl5_privlib}/Filter/Simple.pm
# FindBin.pm
%attr(0444,root,root) %{perl5_privlib}/FindBin.pm
# GDBM_File
%attr(0444,root,root) %{perl5_archlib}/GDBM_File.pm
%dir %{perl5_archlib}/auto/GDBM_File
%attr(0555,root,root) %{perl5_archlib}/auto/GDBM_File/GDBM_File.so
# Getopt
%dir %{perl5_privlib}/Getopt
%attr(0444,root,root) %{perl5_privlib}/Getopt/Long.pm
%attr(0444,root,root) %{perl5_privlib}/Getopt/Std.pm
# Hash
%dir %{perl5_archlib}/Hash
%attr(0444,root,root) %{perl5_archlib}/Hash/Util.pm
%dir %{perl5_archlib}/Hash/Util
%attr(0444,root,root) %{perl5_archlib}/Hash/Util/FieldHash.pm
%dir %{perl5_archlib}/auto/Hash
%dir %{perl5_archlib}/auto/Hash/Util
%attr(0555,root,root) %{perl5_archlib}/auto/Hash/Util/Util.so
%dir %{perl5_archlib}/auto/Hash/Util/FieldHash
%attr(0555,root,root) %{perl5_archlib}/auto/Hash/Util/FieldHash/FieldHash.so
# HTTP
%dir %{perl5_privlib}/HTTP
%attr(0444,root,root) %{perl5_privlib}/HTTP/Tiny.pm
# I18N
%dir %{perl5_archlib}/I18N
%attr(0444,root,root) %{perl5_archlib}/I18N/Langinfo.pm
%dir %{perl5_archlib}/auto/I18N
%dir %{perl5_archlib}/auto/I18N/Langinfo
%attr(0555,root,root) %{perl5_archlib}/auto/I18N/Langinfo/Langinfo.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/I18N
%endif
%attr(0444,root,root) %{perl5_privlib}/I18N/Collate.pm
%attr(0444,root,root) %{perl5_privlib}/I18N/LangTags.pm
%dir %{perl5_privlib}/I18N/LangTags
%attr(0444,root,root) %{perl5_privlib}/I18N/LangTags/Detect.pm
%attr(0444,root,root) %{perl5_privlib}/I18N/LangTags/List.pm 
# IO
%attr(0444,root,root) %{perl5_archlib}/IO.pm
%dir %{perl5_archlib}/IO
%attr(0444,root,root) %{perl5_archlib}/IO/Dir.pm
%attr(0444,root,root) %{perl5_archlib}/IO/File.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Handle.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Pipe.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Poll.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Seekable.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Select.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Socket.pm
%dir %{perl5_archlib}/IO/Socket
%attr(0444,root,root) %{perl5_archlib}/IO/Socket/INET.pm
%attr(0444,root,root) %{perl5_archlib}/IO/Socket/UNIX.pm
%dir %{perl5_archlib}/auto/IO
%attr(0555,root,root) %{perl5_archlib}/auto/IO/IO.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/IO
%dir %{perl5_privlib}/IO/Socket
%endif
%dir %{perl5_privlib}/IO/Compress
%dir %{perl5_privlib}/IO/Compress/Adapter
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Adapter/Bzip2.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Adapter/Deflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Adapter/Identity.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Base.pm
%dir %{perl5_privlib}/IO/Compress/Base
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Base/Common.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Bzip2.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Deflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/FAQ.pod
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Gzip.pm
%dir %{perl5_privlib}/IO/Compress/Gzip
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Gzip/Constants.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/RawDeflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Zip.pm
%dir %{perl5_privlib}/IO/Compress/Zip
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Zip/Constants.pm
%dir %{perl5_privlib}/IO/Compress/Zlib
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Zlib/Constants.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Compress/Zlib/Extra.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Socket/IP.pm
%dir %{perl5_privlib}/IO/Uncompress
%dir %{perl5_privlib}/IO/Uncompress/Adapter
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Adapter/Bunzip2.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Adapter/Identity.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Adapter/Inflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/AnyInflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/AnyUncompress.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Base.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Bunzip2.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Gunzip.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Inflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/RawInflate.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Uncompress/Unzip.pm
%attr(0444,root,root) %{perl5_privlib}/IO/Zlib.pm
# IPC
%dir %{perl5_archlib}/IPC
%attr(0444,root,root) %{perl5_archlib}/IPC/Msg.pm
%attr(0444,root,root) %{perl5_archlib}/IPC/Semaphore.pm
%attr(0444,root,root) %{perl5_archlib}/IPC/SharedMem.pm
%attr(0444,root,root) %{perl5_archlib}/IPC/SysV.pm
%dir %{perl5_archlib}/auto/IPC
%dir %{perl5_archlib}/auto/IPC/SysV
%attr(0555,root,root) %{perl5_archlib}/auto/IPC/SysV/SysV.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/IPC
%endif
%attr(0444,root,root) %{perl5_privlib}/IPC/Cmd.pm
%attr(0444,root,root) %{perl5_privlib}/IPC/Open2.pm
%attr(0444,root,root) %{perl5_privlib}/IPC/Open3.pm
# Internals.pod
%attr(0444,root,root) %{perl5_privlib}/Internals.pod
# JSON
%dir %{perl5_privlib}/JSON
%attr(0444,root,root) %{perl5_privlib}/JSON/PP.pm
%dir %{perl5_privlib}/JSON/PP
%attr(0444,root,root) %{perl5_privlib}/JSON/PP/Boolean.pm
# List
%dir %{perl5_archlib}/List
%attr(0444,root,root) %{perl5_archlib}/List/Util.pm
%dir %{perl5_archlib}/List/Util
%attr(0444,root,root) %{perl5_archlib}/List/Util/XS.pm
%dir %{perl5_archlib}/auto/List
%dir %{perl5_archlib}/auto/List/Util
%attr(0555,root,root) %{perl5_archlib}/auto/List/Util/Util.so
# Locale
%dir %{perl5_privlib}/Locale
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext.pm
%dir %{perl5_privlib}/Locale/Maketext
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext/Cookbook.pod
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext/Guts.pm
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext/GutsLoader.pm
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext/Simple.pm
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext/TPJ13.pod
%attr(0444,root,root) %{perl5_privlib}/Locale/Maketext.pod
# MIME
%dir %{perl5_archlib}/MIME
%attr(0444,root,root) %{perl5_archlib}/MIME/Base64.pm
%attr(0444,root,root) %{perl5_archlib}/MIME/QuotedPrint.pm
%dir %{perl5_archlib}/auto/MIME
%dir %{perl5_archlib}/auto/MIME/Base64
%attr(0555,root,root) %{perl5_archlib}/auto/MIME/Base64/Base64.so
# Math
%dir %{perl5_archlib}/Math
%dir %{perl5_archlib}/Math/BigInt
%attr(0444,root,root) %{perl5_archlib}/Math/BigInt/FastCalc.pm
%dir %{perl5_archlib}/auto/Math
%dir %{perl5_archlib}/auto/Math/BigInt
%dir %{perl5_archlib}/auto/Math/BigInt/FastCalc
%attr(0555,root,root) %{perl5_archlib}/auto/Math/BigInt/FastCalc/FastCalc.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Math
%dir %{perl5_privlib}/Math/BigInt
%endif
%attr(0444,root,root) %{perl5_privlib}/Math/BigFloat.pm
%dir %{perl5_privlib}/Math/BigFloat
%attr(0444,root,root) %{perl5_privlib}/Math/BigFloat/Trace.pm
%attr(0444,root,root) %{perl5_privlib}/Math/BigInt.pm
%attr(0444,root,root) %{perl5_privlib}/Math/BigInt/Calc.pm
%attr(0444,root,root) %{perl5_privlib}/Math/BigInt/Lib.pm
%attr(0444,root,root) %{perl5_privlib}/Math/BigInt/Trace.pm
%attr(0444,root,root) %{perl5_privlib}/Math/BigRat.pm
%dir %{perl5_privlib}/Math/BigRat
%attr(0444,root,root) %{perl5_privlib}/Math/BigRat/Trace.pm
%attr(0444,root,root) %{perl5_privlib}/Math/Complex.pm
%attr(0444,root,root) %{perl5_privlib}/Math/Trig.pm
# Memoize
%attr(0444,root,root) %{perl5_privlib}/Memoize.pm
%dir %{perl5_privlib}/Memoize
%attr(0444,root,root) %{perl5_privlib}/Memoize/AnyDBM_File.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/Expire.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/ExpireFile.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/ExpireTest.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/NDBM_File.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/SDBM_File.pm
%attr(0444,root,root) %{perl5_privlib}/Memoize/Storable.pm
# Module
%dir %{perl5_privlib}/Module
%attr(0444,root,root) %{perl5_privlib}/Module/CoreList.pm
%dir %{perl5_privlib}/Module/CoreList
%attr(0444,root,root) %{perl5_privlib}/Module/CoreList/Utils.pm
%attr(0444,root,root) %{perl5_privlib}/Module/CoreList.pod
%attr(0444,root,root) %{perl5_privlib}/Module/Load.pm
%dir %{perl5_privlib}/Module/Load
%attr(0444,root,root) %{perl5_privlib}/Module/Load/Conditional.pm
%attr(0444,root,root) %{perl5_privlib}/Module/Loaded.pm
%attr(0444,root,root) %{perl5_privlib}/Module/Metadata.pm
# NDBM_File
%attr(0444,root,root) %{perl5_archlib}/NDBM_File.pm
%dir %{perl5_archlib}/auto/NDBM_File
%attr(0555,root,root) %{perl5_archlib}/auto/NDBM_File/NDBM_File.so
# NEXT.pm
%attr(0444,root,root) %{perl5_privlib}/NEXT.pm
# Net
%dir %{perl5_privlib}/Net
%attr(0444,root,root) %{perl5_privlib}/Net/*.pm
%attr(0444,root,root) %{perl5_privlib}/Net/libnetFAQ.pod
%dir %{perl5_privlib}/Net/FTP
%attr(0444,root,root) %{perl5_privlib}/Net/FTP/*.pm
# O
%attr(0444,root,root) %{perl5_archlib}/O.pm
# ODBM_FILE
%attr(0444,root,root) %{perl5_archlib}/ODBM_File.pm
%dir %{perl5_archlib}/auto/ODBM_File
%attr(0555,root,root) %{perl5_archlib}/auto/ODBM_File/ODBM_File.so
# Opcode
%attr(0444,root,root) %{perl5_archlib}/Opcode.pm
%dir %{perl5_archlib}/auto/Opcode
%attr(0555,root,root) %{perl5_archlib}/auto/Opcode/Opcode.so
# POSIX
%attr(0444,root,root) %{perl5_archlib}/POSIX.pm
%attr(0444,root,root) %{perl5_archlib}/POSIX.pod
%dir %{perl5_archlib}/auto/POSIX
%attr(0444,root,root) %{perl5_archlib}/auto/POSIX/POSIX.so
# Params
%dir %{perl5_privlib}/Params
%attr(0444,root,root) %{perl5_privlib}/Params/Check.pm
# Parse
%dir %{perl5_privlib}/Parse
%dir %{perl5_privlib}/Parse/CPAN
%attr(0444,root,root) %{perl5_privlib}/Parse/CPAN/Meta.pm
# Perl
%dir %{perl5_privlib}/Perl
%attr(0444,root,root) %{perl5_privlib}/Perl/OSType.pm
# PerlIO
%dir %{perl5_archlib}/PerlIO
%attr(0444,root,root) %{perl5_archlib}/PerlIO/encoding.pm
%attr(0444,root,root) %{perl5_archlib}/PerlIO/mmap.pm
%attr(0444,root,root) %{perl5_archlib}/PerlIO/scalar.pm
%attr(0444,root,root) %{perl5_archlib}/PerlIO/via.pm
%dir %{perl5_archlib}/auto/PerlIO
%dir %{perl5_archlib}/auto/PerlIO/encoding
%attr(0555,root,root) %{perl5_archlib}/auto/PerlIO/encoding/encoding.so
%dir %{perl5_archlib}/auto/PerlIO/mmap
%attr(0555,root,root) %{perl5_archlib}/auto/PerlIO/mmap/mmap.so
%dir %{perl5_archlib}/auto/PerlIO/scalar
%attr(0555,root,root) %{perl5_archlib}/auto/PerlIO/scalar/scalar.so
%dir %{perl5_archlib}/auto/PerlIO/via
%attr(0555,root,root) %{perl5_archlib}/auto/PerlIO/via/via.so
%attr(0444,root,root) %{perl5_privlib}/PerlIO.pm
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/PerlIO
%endif
%dir %{perl5_privlib}/PerlIO/via
%attr(0444,root,root) %{perl5_privlib}/PerlIO/via/QuotedPrint.pm
# Pod
%dir %{perl5_privlib}/Pod
%attr(0444,root,root) %{perl5_privlib}/Pod/Checker.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Escapes.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Functions.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Html.pm
%dir %{perl5_privlib}/Pod/Html
%attr(0444,root,root) %{perl5_privlib}/Pod/Html/Util.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Man.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/ParseLink.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Perldoc.pm
%dir %{perl5_privlib}/Pod/Perldoc
%attr(0444,root,root) %{perl5_privlib}/Pod/Perldoc/*.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Simple.pm
%dir %{perl5_privlib}/Pod/Simple
%attr(0444,root,root) %{perl5_privlib}/Pod/Simple/*.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Simple/Subclassing.pod
%attr(0444,root,root) %{perl5_privlib}/Pod/Simple.pod
%attr(0444,root,root) %{perl5_privlib}/Pod/Text.pm
%dir %{perl5_privlib}/Pod/Text
%attr(0444,root,root) %{perl5_privlib}/Pod/Text/Color.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Text/Overstrike.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Text/Termcap.pm
%attr(0444,root,root) %{perl5_privlib}/Pod/Usage.pm
# SDBM_File
%attr(0444,root,root) %{perl5_archlib}/SDBM_File.pm
%dir %{perl5_archlib}/auto/SDBM_File
%attr(0555,root,root) %{perl5_archlib}/auto/SDBM_File/SDBM_File.so
# Safe.pm
%attr(0444,root,root) %{perl5_privlib}/Safe.pm
# Scalar
%dir %{perl5_archlib}/Scalar
%attr(0444,root,root) %{perl5_archlib}/Scalar/Util.pm
# Search
%dir %{perl5_privlib}/Search
%attr(0444,root,root) %{perl5_privlib}/Search/Dict.pm
# SelectSaver.pm -- SelfLoader.pm
%attr(0444,root,root) %{perl5_privlib}/SelectSaver.pm
%attr(0444,root,root) %{perl5_privlib}/SelfLoader.pm
# Socket
%attr(0444,root,root) %{perl5_archlib}/Socket.pm
%dir %{perl5_archlib}/auto/Socket
%attr(0555,root,root) %{perl5_archlib}/auto/Socket/Socket.so
# Storable
%attr(0444,root,root) %{perl5_archlib}/Storable.pm
%dir %{perl5_archlib}/auto/Storable
%attr(0555,root,root) %{perl5_archlib}/auto/Storable/Storable.so
# Sub
%dir %{perl5_archlib}/Sub
%attr(0444,root,root) %{perl5_archlib}/Sub/Util.pm
# Symbol.pm
%attr(0444,root,root) %{perl5_privlib}/Symbol.pm
# Sys
%dir %{perl5_archlib}/Sys
%attr(0444,root,root) %{perl5_archlib}/Sys/Hostname.pm
%attr(0444,root,root) %{perl5_archlib}/Sys/Syslog.pm
%dir %{perl5_archlib}/auto/Sys/Hostname
%attr(0555,root,root) %{perl5_archlib}/auto/Sys/Hostname/Hostname.so
%dir %{perl5_archlib}/auto/Sys/Syslog
%attr(0555,root,root) %{perl5_archlib}/auto/Sys/Syslog/Syslog.so
# TAP
%dir %{perl5_privlib}/TAP
%attr(0444,root,root) %{perl5_privlib}/TAP/Base.pm
%dir %{perl5_privlib}/TAP/Formatter
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Base.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Color.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Console.pm
%dir %{perl5_privlib}/TAP/Formatter/Console
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Console/ParallelSession.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Console/Session.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/File.pm
%dir %{perl5_privlib}/TAP/Formatter/File
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/File/Session.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Formatter/Session.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Harness.pm
%dir %{perl5_privlib}/TAP/Harness
%attr(0444,root,root) %{perl5_privlib}/TAP/Harness/Beyond.pod
%attr(0444,root,root) %{perl5_privlib}/TAP/Harness/Env.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Object.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser.pm
%dir %{perl5_privlib}/TAP/Parser
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Aggregator.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Grammar.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Iterator.pm
%dir %{perl5_privlib}/TAP/Parser/Iterator
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Iterator/Array.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Iterator/Process.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Iterator/Stream.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/IteratorFactory.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Multiplexer.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result.pm
%dir %{perl5_privlib}/TAP/Parser/Result
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Bailout.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Comment.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Plan.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Pragma.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Test.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Unknown.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/Version.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Result/YAML.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/ResultFactory.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Scheduler.pm
%dir %{perl5_privlib}/TAP/Parser/Scheduler
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Scheduler/Job.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Scheduler/Spinner.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/Source.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler.pm
%dir %{perl5_privlib}/TAP/Parser/SourceHandler
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler/Executable.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler/File.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler/Handle.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler/Perl.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/SourceHandler/RawTAP.pm
%dir %{perl5_privlib}/TAP/Parser/YAMLish
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/YAMLish/Reader.pm
%attr(0444,root,root) %{perl5_privlib}/TAP/Parser/YAMLish/Writer.pm
#term
%dir %{perl5_privlib}/Term
%attr(0444,root,root) %{perl5_privlib}/Term/ANSIColor.pm
%attr(0444,root,root) %{perl5_privlib}/Term/Cap.pm
%attr(0444,root,root) %{perl5_privlib}/Term/Complete.pm
%attr(0444,root,root) %{perl5_privlib}/Term/ReadLine.pm
# Test
%attr(0444,root,root) %{perl5_privlib}/Test.pm
%dir %{perl5_privlib}/Test
%attr(0444,root,root) %{perl5_privlib}/Test/Builder.pm
%dir %{perl5_privlib}/Test/Builder
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/Formatter.pm
%dir %{perl5_privlib}/Test/Builder/IO
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/IO/Scalar.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/Module.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/Tester.pm
%dir %{perl5_privlib}/Test/Builder/Tester
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/Tester/Color.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Builder/TodoDiag.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Harness.pm
%attr(0444,root,root) %{perl5_privlib}/Test/More.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Simple.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Tester.pm
%dir %{perl5_privlib}/Test/Tester
%attr(0444,root,root) %{perl5_privlib}/Test/Tester/Capture.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Tester/CaptureRunner.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Tester/Delegate.pm
%attr(0444,root,root) %{perl5_privlib}/Test/Tutorial.pod
%dir %{perl5_privlib}/Test/use
%attr(0444,root,root) %{perl5_privlib}/Test/use/ok.pm
# Test2
%attr(0444,root,root) %{perl5_privlib}/Test2.pm
%dir %{perl5_privlib}/Test2
%attr(0444,root,root) %{perl5_privlib}/Test2/API.pm
%dir %{perl5_privlib}/Test2/API
%attr(0444,root,root) %{perl5_privlib}/Test2/API/Breakage.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/Context.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/Instance.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/InterceptResult.pm
%dir %{perl5_privlib}/Test2/API/InterceptResult
%attr(0444,root,root) %{perl5_privlib}/Test2/API/InterceptResult/Event.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/InterceptResult/Facet.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/InterceptResult/Hub.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/InterceptResult/Squasher.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/API/Stack.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event.pm
%dir %{perl5_privlib}/Test2/Event
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Bail.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Diag.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Encoding.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Exception.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Fail.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Generic.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Note.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Ok.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Pass.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Plan.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Skip.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Subtest.pm
%dir %{perl5_privlib}/Test2/Event/TAP
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/TAP/Version.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/V2.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Event/Waiting.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet.pm
%dir %{perl5_privlib}/Test2/EventFacet
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/About.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Amnesty.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Assert.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Control.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Error.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Hub.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Info.pm
%dir %{perl5_privlib}/Test2/EventFacet/Info
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Info/Table.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Meta.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Parent.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Plan.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Render.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/EventFacet/Trace.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Formatter.pm
%dir %{perl5_privlib}/Test2/Formatter
%attr(0444,root,root) %{perl5_privlib}/Test2/Formatter/TAP.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Hub.pm
%dir %{perl5_privlib}/Test2/Hub
%attr(0444,root,root) %{perl5_privlib}/Test2/Hub/Interceptor.pm
%dir %{perl5_privlib}/Test2/Hub/Interceptor
%attr(0444,root,root) %{perl5_privlib}/Test2/Hub/Interceptor/Terminator.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Hub/Subtest.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/IPC.pm
%dir %{perl5_privlib}/Test2/IPC
%attr(0444,root,root) %{perl5_privlib}/Test2/IPC/Driver.pm
%dir %{perl5_privlib}/Test2/IPC/Driver
%attr(0444,root,root) %{perl5_privlib}/Test2/IPC/Driver/Files.pm
%dir %{perl5_privlib}/Test2/Tools
%attr(0444,root,root) %{perl5_privlib}/Test2/Tools/Tiny.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Transition.pod
%attr(0444,root,root) %{perl5_privlib}/Test2/Util.pm
%dir %{perl5_privlib}/Test2/Util
%attr(0444,root,root) %{perl5_privlib}/Test2/Util/ExternalMeta.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Util/Facets2Legacy.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Util/HashBase.pm
%attr(0444,root,root) %{perl5_privlib}/Test2/Util/Trace.pm
# Text
%dir %{perl5_privlib}/Text
%attr(0444,root,root) %{perl5_privlib}/Text/Abbrev.pm
%attr(0444,root,root) %{perl5_privlib}/Text/Balanced.pm
%attr(0444,root,root) %{perl5_privlib}/Text/ParseWords.pm
%attr(0444,root,root) %{perl5_privlib}/Text/Tabs.pm
%attr(0444,root,root) %{perl5_privlib}/Text/Wrap.pm
# Thread
%attr(0444,root,root) %{perl5_privlib}/Thread.pm
%dir %{perl5_privlib}/Thread
%attr(0444,root,root) %{perl5_privlib}/Thread/Queue.pm
%attr(0444,root,root) %{perl5_privlib}/Thread/Semaphore.pm
# Tie
%dir %{perl5_privlib}/Tie
%attr(0444,root,root) %{perl5_privlib}/Tie/Array.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/File.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/Handle.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/Hash.pm
%dir %{perl5_privlib}/Tie/Hash
%attr(0444,root,root) %{perl5_privlib}/Tie/Hash/NamedCapture.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/Memoize.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/RefHash.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/Scalar.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/StdHandle.pm
%attr(0444,root,root) %{perl5_privlib}/Tie/SubstrHash.pm
# Time
%dir %{perl5_archlib}/Time
%attr(0444,root,root) %{perl5_archlib}/Time/HiRes.pm
%attr(0444,root,root) %{perl5_archlib}/Time/Piece.pm
%attr(0444,root,root) %{perl5_archlib}/Time/Seconds.pm
%dir %{perl5_archlib}/auto/Time
%dir %{perl5_archlib}/auto/Time/HiRes
%attr(0555,root,root) %{perl5_archlib}/auto/Time/HiRes/HiRes.so
%dir %{perl5_archlib}/auto/Time/Piece
%attr(0555,root,root) %{perl5_archlib}/auto/Time/Piece/Piece.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Time
%endif
%attr(0444,root,root) %{perl5_privlib}/Time/Local.pm
%attr(0444,root,root) %{perl5_privlib}/Time/gmtime.pm
%attr(0444,root,root) %{perl5_privlib}/Time/localtime.pm
%attr(0444,root,root) %{perl5_privlib}/Time/tm.pm
# UNIVERSAL.pm
%attr(0444,root,root) %{perl5_privlib}/UNIVERSAL.pm
# Unicode
%dir %{perl5_archlib}/Unicode
%attr(0444,root,root) %{perl5_archlib}/Unicode/Collate.pm
%dir %{perl5_archlib}/Unicode/Collate
%attr(0444,root,root) %{perl5_archlib}/Unicode/Collate/Locale.pm
%attr(0444,root,root) %{perl5_archlib}/Unicode/Normalize.pm
%dir %{perl5_archlib}/auto/Unicode
%dir %{perl5_archlib}/auto/Unicode/Collate
%attr(0555,root,root) %{perl5_archlib}/auto/Unicode/Collate/Collate.so
%dir %{perl5_archlib}/auto/Unicode/Normalize
%attr(0555,root,root) %{perl5_archlib}/auto/Unicode/Normalize/Normalize.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_privlib}/Unicode
%dir %{perl5_privlib}/Unicode/Collate
%endif
%dir %{perl5_privlib}/Unicode/Collate/CJK
%attr(0444,root,root) %{perl5_privlib}/Unicode/Collate/CJK/*.pm
%dir %{perl5_privlib}/Unicode/Collate/Locale
%attr(0444,root,root) %{perl5_privlib}/Unicode/Collate/Locale/*.pl
%attr(0444,root,root) %{perl5_privlib}/Unicode/Collate/allkeys.txt
%attr(0444,root,root) %{perl5_privlib}/Unicode/Collate/keys.txt
%attr(0444,root,root) %{perl5_privlib}/Unicode/UCD.pm
# User
%dir %{perl5_privlib}/User
%attr(0444,root,root) %{perl5_privlib}/User/grent.pm
%attr(0444,root,root) %{perl5_privlib}/User/pwent.pm
# XSLoader.pm -- _charnames.pm
%attr(0444,root,root) %{perl5_privlib}/XSLoader.pm
%attr(0444,root,root) %{perl5_privlib}/_charnames.pm
# attributes
%attr(0444,root,root) %{perl5_archlib}/attributes.pm
%dir %{perl5_archlib}/auto/attributes
%attr(0555,root,root) %{perl5_archlib}/auto/attributes/attributes.so
# autodie
%attr(0444,root,root) %{perl5_privlib}/autodie.pm
%dir %{perl5_privlib}/autodie
%dir %{perl5_privlib}/autodie/Scope
%attr(0444,root,root) %{perl5_privlib}/autodie/Scope/Guard.pm
%attr(0444,root,root) %{perl5_privlib}/autodie/Scope/GuardStack.pm
%attr(0444,root,root) %{perl5_privlib}/autodie/Util.pm
%attr(0444,root,root) %{perl5_privlib}/autodie/exception.pm
%dir %{perl5_privlib}/autodie/exception
%attr(0444,root,root) %{perl5_privlib}/autodie/exception/system.pm
%attr(0444,root,root) %{perl5_privlib}/autodie/hints.pm
%attr(0444,root,root) %{perl5_privlib}/autodie/skip.pm
# autouse.pm -- dumpvar.pl
%attr(0444,root,root) %{perl5_privlib}/autouse.pm
%attr(0444,root,root) %{perl5_privlib}/base.pm
%attr(0444,root,root) %{perl5_privlib}/bigfloat.pm
%attr(0444,root,root) %{perl5_privlib}/bigint.pm
%attr(0444,root,root) %{perl5_privlib}/bignum.pm
%attr(0444,root,root) %{perl5_privlib}/bigrat.pm
%attr(0444,root,root) %{perl5_privlib}/blib.pm
%attr(0444,root,root) %{perl5_privlib}/builtin.pm
%attr(0444,root,root) %{perl5_privlib}/bytes.pm
%attr(0444,root,root) %{perl5_privlib}/bytes_heavy.pl
%attr(0444,root,root) %{perl5_privlib}/charnames.pm
%attr(0444,root,root) %{perl5_privlib}/constant.pm
%attr(0444,root,root) %{perl5_privlib}/deprecate.pm
%attr(0444,root,root) %{perl5_privlib}/diagnostics.pm
%attr(0444,root,root) %{perl5_privlib}/dumpvar.pl
# encoding
%attr(0444,root,root) %{perl5_archlib}/encoding.pm
%dir %{perl5_privlib}/encoding
%attr(0444,root,root) %{perl5_privlib}/encoding/warnings.pm
# experimental.pm -- less.pm
%attr(0444,root,root) %{perl5_privlib}/experimental.pm
%attr(0444,root,root) %{perl5_privlib}/feature.pm
%attr(0444,root,root) %{perl5_privlib}/fields.pm
%attr(0444,root,root) %{perl5_privlib}/filetest.pm
%attr(0444,root,root) %{perl5_privlib}/if.pm
%attr(0444,root,root) %{perl5_privlib}/integer.pm
%attr(0444,root,root) %{perl5_privlib}/less.pm
# lib
%attr(0444,root,root) %{perl5_archlib}/lib.pm
# locale.pm
%attr(0444,root,root) %{perl5_privlib}/locale.pm
# meta_notation.pm
%attr(0444,root,root) %{perl5_privlib}/meta_notation.pm
# mro
%attr(0444,root,root) %{perl5_archlib}/mro.pm
%dir %{perl5_archlib}/auto/mro
%attr(0555,root,root) %{perl5_archlib}/auto/mro/mro.so
# ok.pm
%attr(0444,root,root) %{perl5_privlib}/ok.pm
# open.pm
%attr(0444,root,root) %{perl5_privlib}/open.pm
# ops
%attr(0444,root,root) %{perl5_archlib}/ops.pm
# overload
%attr(0444,root,root) %{perl5_privlib}/overload.pm
%dir %{perl5_privlib}/overload
%attr(0444,root,root) %{perl5_privlib}/overload/numbers.pm
%attr(0444,root,root) %{perl5_privlib}/overloading.pm
# parent.pm
%attr(0444,root,root) %{perl5_privlib}/parent.pm
# perl5db.pl
%attr(0444,root,root) %{perl5_privlib}/perl5db.pl
# perlfaq.pm
%attr(0444,root,root) %{perl5_privlib}/perlfaq.pm
# re
%attr(0444,root,root) %{perl5_archlib}/re.pm
%dir %{perl5_archlib}/auto/re
%attr(0555,root,root) %{perl5_archlib}/auto/re/re.so
# sigtrap.pm
%attr(0444,root,root) %{perl5_privlib}/sigtrap.pm
# sort.pm
%attr(0444,root,root) %{perl5_privlib}/sort.pm
# strict.pm
%attr(0444,root,root) %{perl5_privlib}/strict.pm
# subs.pm
%attr(0444,root,root) %{perl5_privlib}/subs.pm
# threads
%attr(0444,root,root) %{perl5_archlib}/threads.pm
%dir %{perl5_archlib}/threads
%attr(0444,root,root) %{perl5_archlib}/threads/shared.pm
%dir %{perl5_archlib}/auto/threads
%attr(0555,root,root) %{perl5_archlib}/auto/threads/threads.so
%dir %{perl5_archlib}/auto/threads/shared
%attr(0555,root,root) %{perl5_archlib}/auto/threads/shared/shared.so
# unicore
%dir %{perl5_privlib}/unicore
%attr(0444,root,root) %{perl5_privlib}/unicore/Blocks.txt
%attr(0444,root,root) %{perl5_privlib}/unicore/CombiningClass.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/Decomposition.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/Name.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/Name.pm
%attr(0444,root,root) %{perl5_privlib}/unicore/NamedSequences.txt
%attr(0444,root,root) %{perl5_privlib}/unicore/SpecialCasing.txt
%attr(0444,root,root) %{perl5_privlib}/unicore/UCD.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/uni_keywords.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/version
%dir %{perl5_privlib}/unicore/To
%attr(0444,root,root) %{perl5_privlib}/unicore/To/*.pl
%dir %{perl5_privlib}/unicore/lib
%dir %{perl5_privlib}/unicore/lib/Age
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Age/*.pl
%dir %{perl5_privlib}/unicore/lib/Alpha
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Alpha/Y.pl
%dir %{perl5_privlib}/unicore/lib/Bc
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Bc/*.pl
%dir %{perl5_privlib}/unicore/lib/BidiC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/BidiC/Y.pl
%dir %{perl5_privlib}/unicore/lib/BidiM
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/BidiM/Y.pl
%dir %{perl5_privlib}/unicore/lib/Blk
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Blk/NB.pl
%dir %{perl5_privlib}/unicore/lib/Bpt
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Bpt/*.pl
%dir %{perl5_privlib}/unicore/lib/CE
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CE/Y.pl
%dir %{perl5_privlib}/unicore/lib/CI
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CI/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWCF
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWCF/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWCM
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWCM/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWKCF
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWKCF/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWL
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWL/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWT
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWT/Y.pl
%dir %{perl5_privlib}/unicore/lib/CWU
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CWU/Y.pl
%dir %{perl5_privlib}/unicore/lib/Cased
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Cased/Y.pl
%dir %{perl5_privlib}/unicore/lib/Ccc
%attr(0644,root,root) %{perl5_privlib}/unicore/lib/Ccc/*.pl
%dir %{perl5_privlib}/unicore/lib/CompEx
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/CompEx/Y.pl
%dir %{perl5_privlib}/unicore/lib/DI
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/DI/Y.pl
%dir %{perl5_privlib}/unicore/lib/Dash
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Dash/Y.pl
%dir %{perl5_privlib}/unicore/lib/Dep
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Dep/Y.pl
%dir %{perl5_privlib}/unicore/lib/Dia
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Dia/Y.pl
%dir %{perl5_privlib}/unicore/lib/Dt
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Dt/*.pl
%dir %{perl5_privlib}/unicore/lib/EBase
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/EBase/Y.pl
%dir %{perl5_privlib}/unicore/lib/EComp
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/EComp/Y.pl
%dir %{perl5_privlib}/unicore/lib/EPres
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/EPres/Y.pl
%dir %{perl5_privlib}/unicore/lib/Ea
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Ea/*.pl
%dir %{perl5_privlib}/unicore/lib/Emoji
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Emoji/Y.pl
%dir %{perl5_privlib}/unicore/lib/Ext
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Ext/Y.pl
%dir %{perl5_privlib}/unicore/lib/ExtPict
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/ExtPict/Y.pl
%dir %{perl5_privlib}/unicore/lib/GCB
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/GCB/*.pl
%dir %{perl5_privlib}/unicore/lib/Gc
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Gc/*.pl
%dir %{perl5_privlib}/unicore/lib/GrBase
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/GrBase/Y.pl
%dir %{perl5_privlib}/unicore/lib/GrExt
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/GrExt/Y.pl
%dir %{perl5_privlib}/unicore/lib/Hex
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Hex/Y.pl
%dir %{perl5_privlib}/unicore/lib/Hst
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Hst/NA.pl
%dir %{perl5_privlib}/unicore/lib/Hyphen
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Hyphen/T.pl
%dir %{perl5_privlib}/unicore/lib/IDC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/IDC/Y.pl
%dir %{perl5_privlib}/unicore/lib/IDS
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/IDS/Y.pl
%dir %{perl5_privlib}/unicore/lib/IdStatus
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/IdStatus/Allowed.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/IdStatus/Restrict.pl
%dir %{perl5_privlib}/unicore/lib/IdType
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/IdType/*.pl
%dir %{perl5_privlib}/unicore/lib/Ideo
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Ideo/Y.pl
%dir %{perl5_privlib}/unicore/lib/In
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/In/*.pl
%dir %{perl5_privlib}/unicore/lib/InPC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/InPC/*.pl
%dir %{perl5_privlib}/unicore/lib/InSC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/InSC/*.pl
%dir %{perl5_privlib}/unicore/lib/Jg
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Jg/*.pl
%dir %{perl5_privlib}/unicore/lib/Jt
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Jt/*.pl
%dir %{perl5_privlib}/unicore/lib/Lb
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Lb/*.pl
%dir %{perl5_privlib}/unicore/lib/Lower
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Lower/Y.pl
%dir %{perl5_privlib}/unicore/lib/Math
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Math/Y.pl
%dir %{perl5_privlib}/unicore/lib/NFCQC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFCQC/M.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFCQC/Y.pl
%dir %{perl5_privlib}/unicore/lib/NFDQC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFDQC/N.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFDQC/Y.pl
%dir %{perl5_privlib}/unicore/lib/NFKCQC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFKCQC/N.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFKCQC/Y.pl
%dir %{perl5_privlib}/unicore/lib/NFKDQC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFKDQC/N.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/NFKDQC/Y.pl
%dir %{perl5_privlib}/unicore/lib/Nt
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Nt/Di.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Nt/None.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Nt/Nu.pl
%dir %{perl5_privlib}/unicore/lib/Nv
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Nv/*.pl
%dir %{perl5_privlib}/unicore/lib/PCM
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/PCM/Y.pl
%dir %{perl5_privlib}/unicore/lib/PatSyn
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/PatSyn/Y.pl
%dir %{perl5_privlib}/unicore/lib/Perl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Perl/*.pl
%dir %{perl5_privlib}/unicore/lib/QMark
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/QMark/Y.pl
%dir %{perl5_privlib}/unicore/lib/SB
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/SB/*.pl
%dir %{perl5_privlib}/unicore/lib/SD
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/SD/Y.pl
%dir %{perl5_privlib}/unicore/lib/STerm
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/STerm/Y.pl
%dir %{perl5_privlib}/unicore/lib/Sc
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Sc/*.pl
%dir %{perl5_privlib}/unicore/lib/Scx
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Scx/*.pl
%dir %{perl5_privlib}/unicore/lib/Term
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Term/Y.pl
%dir %{perl5_privlib}/unicore/lib/UIdeo
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/UIdeo/Y.pl
%dir %{perl5_privlib}/unicore/lib/Upper
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Upper/Y.pl
%dir %{perl5_privlib}/unicore/lib/VS
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/VS/Y.pl
%dir %{perl5_privlib}/unicore/lib/Vo
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Vo/R.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Vo/Tr.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Vo/Tu.pl
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/Vo/U.pl
%dir %{perl5_privlib}/unicore/lib/WB
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/WB/*.pl
%dir %{perl5_privlib}/unicore/lib/XIDC
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/XIDC/Y.pl
%dir %{perl5_privlib}/unicore/lib/XIDS
%attr(0444,root,root) %{perl5_privlib}/unicore/lib/XIDS/Y.pl
# utf8
%attr(0444,root,root) %{perl5_privlib}/utf8.pm
# vars
%attr(0444,root,root) %{perl5_privlib}/vars.pm
# version
%attr(0444,root,root) %{perl5_privlib}/version.pm
%attr(0444,root,root) %{perl5_privlib}/version.pod
%dir %{perl5_privlib}/version
%attr(0444,root,root) %{perl5_privlib}/version/Internals.pod
%attr(0444,root,root) %{perl5_privlib}/version/regex.pm
# vmsish
%attr(0444,root,root) %{perl5_privlib}/vmsish.pm
# warnings
%attr(0444,root,root) %{perl5_privlib}/warnings.pm
%dir %{perl5_privlib}/warnings
%attr(0444,root,root) %{perl5_privlib}/warnings/register.pm
#
# ???
%{perl5_archlib}/.packlist
#
# pod - may need refinement
%dir %{perl5_privlib}/pod
%attr(0644,root,root) %{perl5_privlib}/pod/*.pod
#man pages
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%license Artistic Copying README
%doc %{name}-make.test.log
%doc Artistic Copying AUTHORS README README.linux


%changelog
* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev2
- Fix packaging bug (wrong perms on a few directories), filter out
-  bogus requires, enable stripping.

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
