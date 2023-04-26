# WARNING - subpackages have different
#  versions that perl so always use a
#  an incremented specrel even when
#  updating perl5_patch (e.g. for
#  5.36.0 to 5.36.1)
%global specrel 0.dev9
# Version definitions
%global perl5_version 5.36
%global perl5_patch 1
%global perl5_epoch 2
%global rpmperlv %{perl5_version}.%{perl5_patch}

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

# General macros
%global __perl /usr/bin/perl
%global perl5 %__perl
%global perl5_corelib    %{_prefix}/lib/perl5/%{perl5_version}/core_perl
%global perl5_corearch   %{_libdir}/perl5/%{perl5_version}/core_perl
%global perl5_sitelib    %{_prefix}/lib/perl5/%{perl5_version}/site_perl
%global perl5_sitearch   %{_libdir}/perl5/%{perl5_version}/site_perl
%global perl5_vendorlib  %{_prefix}/lib/perl5/%{perl5_version}/vendor_perl
%global perl5_vendorarch %{_libdir}/perl5/%{perl5_version}/vendor_perl
# YJL specific macros
%global perl5_cpanlic %{_datadir}/licenses-cpan-common
%global perl5_os_platform %{_arch}-linux-gnu
%global perl5_API Perl-%{perl5_version}
%global perl5_ABI %{perl5_API}-%{perl5_os_platform}

%if "%{_lib}" == "lib64"
%global linuxMultiarch true
%endif

Name:     perl
# Seems that Fedora/RHEL are at epoch 4 ????
#  Epoch 2 seems to be at least needed because of
#  internal perl requires
Epoch:    %{perl5_epoch}
Version:  %{rpmperlv}
Release:  %{?repo}%{specrel}%{?dist}
Summary:  People Hate Perl

Group:    Programming/Languages
License:  GPL-1.0-or-later or Artistic-1.0-Perl
URL:      https://www.perl.org/
Source0:  https://www.cpan.org/src/5.0/perl-%{version}.tar.gz
Source1:  rpm-macros-perl-5.36
Source2:  perl-manlist-%{rpmperlv}.txt
Provides: %{perl5_API}
Provides: %{perl5_ABI}

#BuildRequires:	
Requires:	%{name}-libperl = %{perl5_epoch}:%{rpmperlv}-%{release}

%description
Perl is a highly capable, feature-rich programming language with over
30 years of development. Perl runs on over 100 platforms from portables
to mainframes and is suitable for both rapid prototyping and large scale
development projects.

%package devel
Summary:  Perl development files
Group:    Development/Libraries
Requires: %{name} = %{perl5_epoch}:%{rpmperlv}-%{release}

%description devel
This package contains the perl development tools that are needed to
build perl5 modules. I recommend installing this package even if you
do not think you will need it.

%package libperl
Summary:  The libperl.so library
Group:    System Environment/Libraries
Requires: perl = %{perl5_epoch}:%{rpmperlv}-%{release}

%description libperl
This package contains the libperl.so runtime library.

##########################
#                        #
# Separable Perl Modules #
#                        #
##########################

%package Digest-MD5
Epoch:    0
Version:  2.58
Summary:  Perl interface to the MD5 Algorithm
Group:    System Environment/Libraries
Requires: %{name} = %{perl5_epoch}:%{rpmperlv}-%{release}

%description Digest-MD5
The Digest::MD5 module allows you to use the RSA Data Security Inc. MD5
Message Digest algorithm from within Perl programs. The algorithm takes
as input a message of arbitrary length and produces as output a 128-bit
"fingerprint" or "message digest" of the input.

%package Digest-SHA
Epoch:    0
Version:  6.02
Summary:  Perl extension for SHA-1/224/256/384/512
Group:    System Environment/Libraries
Requires: %{name} = %{perl5_epoch}:%{rpmperlv}-%{release}

%description Digest-SHA
Digest::SHA is a complete implementation of the NIST Secure Hash Standard.
It gives Perl programmers a convenient way to calculate SHA-1, SHA-224,
SHA-256, SHA-384, SHA-512, SHA-512/224, and SHA-512/256 message digests.
The module can handle all types of input, including partial-byte data.

%prep
%setup -q


%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0

sh Configure -des                   \
  -Dprefix=%{_prefix}               \
  -Dvendorprefix=%{_prefix}         \
  -Dprivlib=%{perl5_corelib}        \
  -Darchlib=%{perl5_corearch}        \
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

cp %{SOURCE2} ./manpagelist

##
## /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w
%{_fixperms} %{buildroot}%{perl5_corearch}
%if 0%{?linuxMultiarch:1} == 1
%{_fixperms} %{buildroot}%{perl5_corelib}
%endif

%post libperl -p /sbin/ldconfig
%postun libperl -p /sbin/ldconfig

%files -f manpagelist
%defattr(-,root,root,-)
###
# /usr/bin stuff
###
%attr(0755,root,root) %{_bindir}/corelist
%attr(0755,root,root) %{_bindir}/cpan
%attr(0755,root,root) %{_bindir}/enc2xs
%attr(0755,root,root) %{_bindir}/encguess
%attr(0755,root,root) %{_bindir}/h2ph
#%%attr(0755,root,root) %%{_bindir}/h2xs
%attr(0755,root,root) %{_bindir}/instmodsh
%attr(0755,root,root) %{_bindir}/json_pp
%attr(0755,root,root) %{_bindir}/libnetcfg
%attr(0755,root,root) %{_bindir}/perl
%attr(0755,root,root) %{_bindir}/perl%{rpmperlv}
%attr(0755,root,root) %{_bindir}/perlbug
%attr(0755,root,root) %{_bindir}/perldoc
#%%attr(0755,root,root) %%{_bindir}/perlivp
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
%attr(0444,root,root) %{perl5_corelib}/AnyDBM_File.pm
# App
%dir %{perl5_corelib}/App
%attr(0444,root,root) %{perl5_corelib}/App/Cpan.pm
%attr(0444,root,root) %{perl5_corelib}/App/Prove.pm
%dir %{perl5_corelib}/App/Prove
%attr(0444,root,root) %{perl5_corelib}/App/Prove/State.pm
%dir %{perl5_corelib}/App/Prove/State/
%attr(0444,root,root) %{perl5_corelib}/App/Prove/State/Result.pm
%dir %{perl5_corelib}/App/Prove/State/Result
%attr(0444,root,root) %{perl5_corelib}/App/Prove/State/Result/Test.pm
# Archive
%dir %{perl5_corelib}/Archive
%attr(0444,root,root) %{perl5_corelib}/Archive/Tar.pm
%dir %{perl5_corelib}/Archive/Tar
%attr(0444,root,root) %{perl5_corelib}/Archive/Tar/Constant.pm
%attr(0444,root,root) %{perl5_corelib}/Archive/Tar/File.pm
# Attribute
%dir %{perl5_corelib}/Attribute
%attr(0444,root,root) %{perl5_corelib}/Attribute/Handlers.pm
# AutoLoader.pm -- AutoSplit.pm
%attr(0444,root,root) %{perl5_corelib}/AutoLoader.pm
%attr(0444,root,root) %{perl5_corelib}/AutoSplit.pm
#B
%attr(0444,root,root) %{perl5_corearch}/B.pm
%dir %{perl5_corearch}/B
%attr(0444,root,root) %{perl5_corearch}/B/Concise.pm
%attr(0444,root,root) %{perl5_corearch}/B/Showlex.pm
%attr(0444,root,root) %{perl5_corearch}/B/Terse.pm
%attr(0444,root,root) %{perl5_corearch}/B/Xref.pm
%dir %{perl5_corearch}/auto/B
%attr(0555,root,root) %{perl5_corearch}/auto/B/*.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/B
%endif
%attr(0444,root,root) %{perl5_corelib}/B/Deparse.pm
%attr(0444,root,root) %{perl5_corelib}/B/Op_private.pm
# Benchmark.pm
%attr(0444,root,root) %{perl5_corelib}/Benchmark.pm
#CORE
%dir %{perl5_corearch}/CORE
%attr(0444,root,root) %{perl5_corelib}/CORE.pod
# CPAN
%attr(0444,root,root) %{perl5_corelib}/CPAN.pm
%dir %{perl5_corelib}/CPAN
%dir %{perl5_corelib}/CPAN/API
%attr(0444,root,root) %{perl5_corelib}/CPAN/API/HOWTO.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Author.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Bundle.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/CacheMgr.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Complete.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Debug.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/DeferredCode.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Distribution.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Distroprefs.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Distrostatus.pm
%dir %{perl5_corelib}/CPAN/Exception
%attr(0444,root,root) %{perl5_corelib}/CPAN/Exception/RecursiveDependency.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Exception/blocked_urllist.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Exception/yaml_not_installed.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Exception/yaml_process_error.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/FTP.pm
%dir %{perl5_corelib}/CPAN/FTP
%attr(0444,root,root) %{perl5_corelib}/CPAN/FTP/netrc.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/FirstTime.pm
%dir %{perl5_corelib}/CPAN/HTTP
%attr(0444,root,root) %{perl5_corelib}/CPAN/HTTP/Client.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/HTTP/Credentials.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/HandleConfig.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Index.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/InfoObj.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Kwalify.pm
%dir %{perl5_corelib}/CPAN/Kwalify
%attr(0444,root,root) %{perl5_corelib}/CPAN/Kwalify/distroprefs.dd
%attr(0444,root,root) %{perl5_corelib}/CPAN/Kwalify/distroprefs.yml
%dir %{perl5_corelib}/CPAN/LWP
%attr(0444,root,root) %{perl5_corelib}/CPAN/LWP/UserAgent.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta.pm
%dir %{perl5_corelib}/CPAN/Meta
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Converter.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Feature.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History.pm
%dir %{perl5_corelib}/CPAN/Meta/History
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History/Meta_1_0.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History/Meta_1_1.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History/Meta_1_2.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History/Meta_1_3.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/History/Meta_1_4.pod
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Merge.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Prereqs.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Requirements.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Spec.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/Validator.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Meta/YAML.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Mirrors.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Module.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Nox.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Plugin.pm
%dir %{perl5_corelib}/CPAN/Plugin
%attr(0444,root,root) %{perl5_corelib}/CPAN/Plugin/Specfile.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Prompt.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Queue.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Shell.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Tarzip.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/URL.pm
%attr(0444,root,root) %{perl5_corelib}/CPAN/Version.pm
# Carp
%attr(0444,root,root) %{perl5_corelib}/Carp.pm
%dir %{perl5_corelib}/Carp
%attr(0444,root,root) %{perl5_corelib}/Carp/Heavy.pm
# Class
%dir %{perl5_corelib}/Class
%attr(0444,root,root) %{perl5_corelib}/Class/Struct.pm
#Compress
%dir %{perl5_corearch}/Compress
%dir %{perl5_corearch}/Compress/Raw
%attr(0444,root,root) %{perl5_corearch}/Compress/Raw/Bzip2.pm
%attr(0444,root,root) %{perl5_corearch}/Compress/Raw/Zlib.pm
%dir %{perl5_corearch}/auto/Compress
%dir %{perl5_corearch}/auto/Compress/Raw
%dir %{perl5_corearch}/auto/Compress/Raw/Bzip2
%attr(0555,root,root) %{perl5_corearch}/auto/Compress/Raw/Bzip2/Bzip2.so
%dir %{perl5_corearch}/auto/Compress/Raw/Zlib
%attr(0555,root,root) %{perl5_corearch}/auto/Compress/Raw/Zlib/Zlib.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Compress
%endif
%attr(0444,root,root) %{perl5_corelib}/Compress/Zlib.pm
#Config
%attr(0444,root,root) %{perl5_corearch}/Config.pm
%attr(0444,root,root) %{perl5_corearch}/Config.pod
%attr(0444,root,root) %{perl5_corearch}/Config_git.pl
%attr(0444,root,root) %{perl5_corearch}/Config_heavy.pl
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Config
%endif
%attr(0444,root,root) %{perl5_corelib}/Config/Extensions.pm
%dir %{perl5_corelib}/Config/Perl
%attr(0444,root,root) %{perl5_corelib}/Config/Perl/V.pm
#Cwd
%attr(0444,root,root) %{perl5_corearch}/Cwd.pm
%dir %{perl5_corearch}/auto/Cwd
%attr(0555,root,root) %{perl5_corearch}/auto/Cwd/Cwd.so
# DB.pm
%attr(0444,root,root) %{perl5_corelib}/DB.pm
# DBM_Filter
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter.pm
%dir %{perl5_corelib}/DBM_Filter
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter/compress.pm
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter/encode.pm
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter/int32.pm
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter/null.pm
%attr(0444,root,root) %{perl5_corelib}/DBM_Filter/utf8.pm
#Data
%dir %{perl5_corearch}/Data
%attr(0444,root,root) %{perl5_corearch}/Data/Dumper.pm
%dir %{perl5_corearch}/auto/Data
%dir %{perl5_corearch}/auto/Data/Dumper
%attr(0555,root,root) %{perl5_corearch}/auto/Data/Dumper/Dumper.so
#Devel
%dir %{perl5_corearch}/Devel
%attr(0444,root,root) %{perl5_corearch}/Devel/PPPort.pm
%attr(0444,root,root) %{perl5_corearch}/Devel/Peek.pm
%dir %{perl5_corearch}/auto/Devel
%dir %{perl5_corearch}/auto/Devel/Peek
%attr(0555,root,root) %{perl5_corearch}/auto/Devel/Peek/Peek.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Devel
%endif
%attr(0444,root,root) %{perl5_corelib}/Devel/SelfStubber.pm
# Digest
%attr(0444,root,root) %{perl5_corelib}/Digest.pm
%dir %{perl5_corelib}/Digest
%attr(0444,root,root) %{perl5_corelib}/Digest/base.pm
%attr(0444,root,root) %{perl5_corelib}/Digest/file.pm
# DirHandle.pm -- Dumpvalue.pm
%attr(0444,root,root) %{perl5_corelib}/DirHandle.pm
%attr(0444,root,root) %{perl5_corelib}/Dumpvalue.pm
#DynaLoader
%attr(0444,root,root) %{perl5_corearch}/DynaLoader.pm
#Encode
%attr(0444,root,root) %{perl5_corearch}/Encode.pm
%dir %{perl5_corearch}/Encode
%attr(0444,root,root) %{perl5_corearch}/Encode/Alias.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Byte.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/CJKConstants.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/CN.pm
%dir %{perl5_corearch}/Encode/CN
%attr(0444,root,root) %{perl5_corearch}/Encode/CN/HZ.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Config.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/EBCDIC.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Encoder.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Encoding.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/GSM0338.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Guess.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/JP.pm
%dir %{perl5_corearch}/Encode/JP
%attr(0444,root,root) %{perl5_corearch}/Encode/JP/H2Z.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/JP/JIS7.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/KR.pm
%dir %{perl5_corearch}/Encode/KR
%attr(0444,root,root) %{perl5_corearch}/Encode/KR/2022_KR.pm
%dir %{perl5_corearch}/Encode/MIME
%attr(0444,root,root) %{perl5_corearch}/Encode/MIME/Header.pm
%dir %{perl5_corearch}/Encode/MIME/Header
%attr(0444,root,root) %{perl5_corearch}/Encode/MIME/Header/ISO_2022_JP.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/MIME/Name.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Symbol.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/TW.pm
%attr(0444,root,root) %{perl5_corearch}/Encode/Unicode.pm
%dir %{perl5_corearch}/Encode/Unicode
%attr(0444,root,root) %{perl5_corearch}/Encode/Unicode/UTF7.pm
%dir %{perl5_corearch}/auto/Encode
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/Encode.so
%dir %{perl5_corearch}/auto/Encode/Byte
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/Byte/Byte.so
%dir %{perl5_corearch}/auto/Encode/CN
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/CN/CN.so
%dir %{perl5_corearch}/auto/Encode/EBCDIC
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/EBCDIC/EBCDIC.so
%dir %{perl5_corearch}/auto/Encode/JP
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/JP/JP.so
%dir %{perl5_corearch}/auto/Encode/KR
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/KR/KR.so
%dir %{perl5_corearch}/auto/Encode/Symbol
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/Symbol/Symbol.so
%dir %{perl5_corearch}/auto/Encode/TW
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/TW/TW.so
%dir %{perl5_corearch}/auto/Encode/Unicode
%attr(0555,root,root) %{perl5_corearch}/auto/Encode/Unicode/Unicode.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Encode
%endif
%attr(0444,root,root) %{perl5_corelib}/Encode/Changes.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/ConfigLocal_PM.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/Makefile_PL.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/PerlIO.pod
%attr(0444,root,root) %{perl5_corelib}/Encode/README.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/Supported.pod
%attr(0444,root,root) %{perl5_corelib}/Encode/_PM.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/_T.e2x
%attr(0444,root,root) %{perl5_corelib}/Encode/encode.h
# English.pm -- Env.pm
%attr(0444,root,root) %{perl5_corelib}/English.pm
%attr(0444,root,root) %{perl5_corelib}/Env.pm
# Errno
%attr(0444,root,root) %{perl5_corearch}/Errno.pm
# Exporter
%attr(0444,root,root) %{perl5_corelib}/Exporter.pm
%dir %{perl5_corelib}/Exporter
%attr(0444,root,root) %{perl5_corelib}/Exporter/Heavy.pm
# ExtUtils
%dir %{perl5_corelib}/ExtUtils
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder.pm
%dir %{perl5_corelib}/ExtUtils/CBuilder
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Base.pm
%dir %{perl5_corelib}/ExtUtils/CBuilder/Platform
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/Unix.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/VMS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/Windows.pm
%dir %{perl5_corelib}/ExtUtils/CBuilder/Platform/Windows
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/Windows/BCC.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/Windows/GCC.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/Windows/MSVC.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/aix.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/android.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/cygwin.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/darwin.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/dec_osf.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/CBuilder/Platform/os2.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Command.pm
%dir %{perl5_corelib}/ExtUtils/Command
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Command/MM.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Constant.pm
%dir %{perl5_corelib}/ExtUtils/Constant
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Constant/Base.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Constant/ProxySubs.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Constant/Utils.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Constant/XS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Embed.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Install.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Installed.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Liblist.pm
%dir %{perl5_corelib}/ExtUtils/Liblist
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Liblist/Kid.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MANIFEST.SKIP
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_AIX.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Any.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_BeOS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Cygwin.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_DOS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Darwin.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_MacOS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_NW5.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_OS2.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_OS390.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_QNX.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_UWIN.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Unix.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_VMS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_VOS.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Win32.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MM_Win95.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MY.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker.pm
%dir %{perl5_corelib}/ExtUtils/MakeMaker
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker/Config.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker/FAQ.pod
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker/Locale.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker/Tutorial.pod
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/MakeMaker/version.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Manifest.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Miniperl.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Mkbootstrap.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Mksymlists.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/PL2Bat.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Packlist.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS.pm
%dir %{perl5_corelib}/ExtUtils/ParseXS
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS/Constants.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS/CountLines.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS/Eval.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS/Utilities.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/ParseXS.pod
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Typemaps.pm
%dir %{perl5_corelib}/ExtUtils/Typemaps
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Typemaps/Cmd.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Typemaps/InputMap.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Typemaps/OutputMap.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/Typemaps/Type.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/testlib.pm
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/typemap
%attr(0444,root,root) %{perl5_corelib}/ExtUtils/xsubpp
# Fatal.pm
%attr(0444,root,root) %{perl5_corelib}/Fatal.pm
# Fcntl
%attr(0444,root,root) %{perl5_corearch}/Fcntl.pm
%dir %{perl5_corearch}/auto/Fcntl
%attr(0555,root,root) %{perl5_corearch}/auto/Fcntl/Fcntl.so
# File
%dir %{perl5_corearch}/File
%attr(0444,root,root) %{perl5_corearch}/File/DosGlob.pm
%attr(0444,root,root) %{perl5_corearch}/File/Glob.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec.pm
%dir %{perl5_corearch}/File/Spec
%attr(0444,root,root) %{perl5_corearch}/File/Spec/AmigaOS.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Cygwin.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Epoc.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Functions.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Mac.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/OS2.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Unix.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/VMS.pm
%attr(0444,root,root) %{perl5_corearch}/File/Spec/Win32.pm
%dir %{perl5_corearch}/auto/File
%dir %{perl5_corearch}/auto/File/DosGlob
%attr(0555,root,root) %{perl5_corearch}/auto/File/DosGlob/DosGlob.so
%dir %{perl5_corearch}/auto/File/Glob
%attr(0555,root,root) %{perl5_corearch}/auto/File/Glob/Glob.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/File
%endif
%attr(0444,root,root) %{perl5_corelib}/File/Basename.pm
%attr(0444,root,root) %{perl5_corelib}/File/Compare.pm
%attr(0444,root,root) %{perl5_corelib}/File/Copy.pm
%attr(0444,root,root) %{perl5_corelib}/File/Fetch.pm
%attr(0444,root,root) %{perl5_corelib}/File/Find.pm
%attr(0444,root,root) %{perl5_corelib}/File/GlobMapper.pm
%attr(0444,root,root) %{perl5_corelib}/File/Path.pm
%attr(0444,root,root) %{perl5_corelib}/File/Temp.pm
%attr(0444,root,root) %{perl5_corelib}/File/stat.pm
# FileCache.pm -- FileHandle.pm
%attr(0444,root,root) %{perl5_corelib}/FileCache.pm
%attr(0444,root,root) %{perl5_corelib}/FileHandle.pm
# Filter
%dir %{perl5_corearch}/Filter
%dir %{perl5_corearch}/Filter/Util
%attr(0444,root,root) %{perl5_corearch}/Filter/Util/Call.pm
%dir %{perl5_corearch}/auto/Filter
%dir %{perl5_corearch}/auto/Filter/Util
%dir %{perl5_corearch}/auto/Filter/Util/Call
%attr(0555,root,root) %{perl5_corearch}/auto/Filter/Util/Call/Call.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Filter
%endif
%attr(0444,root,root) %{perl5_corelib}/Filter/Simple.pm
# FindBin.pm
%attr(0444,root,root) %{perl5_corelib}/FindBin.pm
# GDBM_File
%attr(0444,root,root) %{perl5_corearch}/GDBM_File.pm
%dir %{perl5_corearch}/auto/GDBM_File
%attr(0555,root,root) %{perl5_corearch}/auto/GDBM_File/GDBM_File.so
# Getopt
%dir %{perl5_corelib}/Getopt
%attr(0444,root,root) %{perl5_corelib}/Getopt/Long.pm
%attr(0444,root,root) %{perl5_corelib}/Getopt/Std.pm
# Hash
%dir %{perl5_corearch}/Hash
%attr(0444,root,root) %{perl5_corearch}/Hash/Util.pm
%dir %{perl5_corearch}/Hash/Util
%attr(0444,root,root) %{perl5_corearch}/Hash/Util/FieldHash.pm
%dir %{perl5_corearch}/auto/Hash
%dir %{perl5_corearch}/auto/Hash/Util
%attr(0555,root,root) %{perl5_corearch}/auto/Hash/Util/Util.so
%dir %{perl5_corearch}/auto/Hash/Util/FieldHash
%attr(0555,root,root) %{perl5_corearch}/auto/Hash/Util/FieldHash/FieldHash.so
# HTTP
%dir %{perl5_corelib}/HTTP
%attr(0444,root,root) %{perl5_corelib}/HTTP/Tiny.pm
# I18N
%dir %{perl5_corearch}/I18N
%attr(0444,root,root) %{perl5_corearch}/I18N/Langinfo.pm
%dir %{perl5_corearch}/auto/I18N
%dir %{perl5_corearch}/auto/I18N/Langinfo
%attr(0555,root,root) %{perl5_corearch}/auto/I18N/Langinfo/Langinfo.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/I18N
%endif
%attr(0444,root,root) %{perl5_corelib}/I18N/Collate.pm
%attr(0444,root,root) %{perl5_corelib}/I18N/LangTags.pm
%dir %{perl5_corelib}/I18N/LangTags
%attr(0444,root,root) %{perl5_corelib}/I18N/LangTags/Detect.pm
%attr(0444,root,root) %{perl5_corelib}/I18N/LangTags/List.pm 
# IO
%attr(0444,root,root) %{perl5_corearch}/IO.pm
%dir %{perl5_corearch}/IO
%attr(0444,root,root) %{perl5_corearch}/IO/Dir.pm
%attr(0444,root,root) %{perl5_corearch}/IO/File.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Handle.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Pipe.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Poll.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Seekable.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Select.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Socket.pm
%dir %{perl5_corearch}/IO/Socket
%attr(0444,root,root) %{perl5_corearch}/IO/Socket/INET.pm
%attr(0444,root,root) %{perl5_corearch}/IO/Socket/UNIX.pm
%dir %{perl5_corearch}/auto/IO
%attr(0555,root,root) %{perl5_corearch}/auto/IO/IO.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/IO
%dir %{perl5_corelib}/IO/Socket
%endif
%dir %{perl5_corelib}/IO/Compress
%dir %{perl5_corelib}/IO/Compress/Adapter
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Adapter/Bzip2.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Adapter/Deflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Adapter/Identity.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Base.pm
%dir %{perl5_corelib}/IO/Compress/Base
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Base/Common.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Bzip2.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Deflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/FAQ.pod
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Gzip.pm
%dir %{perl5_corelib}/IO/Compress/Gzip
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Gzip/Constants.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/RawDeflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Zip.pm
%dir %{perl5_corelib}/IO/Compress/Zip
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Zip/Constants.pm
%dir %{perl5_corelib}/IO/Compress/Zlib
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Zlib/Constants.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Compress/Zlib/Extra.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Socket/IP.pm
%dir %{perl5_corelib}/IO/Uncompress
%dir %{perl5_corelib}/IO/Uncompress/Adapter
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Adapter/Bunzip2.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Adapter/Identity.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Adapter/Inflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/AnyInflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/AnyUncompress.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Base.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Bunzip2.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Gunzip.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Inflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/RawInflate.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Uncompress/Unzip.pm
%attr(0444,root,root) %{perl5_corelib}/IO/Zlib.pm
# IPC
%dir %{perl5_corearch}/IPC
%attr(0444,root,root) %{perl5_corearch}/IPC/Msg.pm
%attr(0444,root,root) %{perl5_corearch}/IPC/Semaphore.pm
%attr(0444,root,root) %{perl5_corearch}/IPC/SharedMem.pm
%attr(0444,root,root) %{perl5_corearch}/IPC/SysV.pm
%dir %{perl5_corearch}/auto/IPC
%dir %{perl5_corearch}/auto/IPC/SysV
%attr(0555,root,root) %{perl5_corearch}/auto/IPC/SysV/SysV.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/IPC
%endif
%attr(0444,root,root) %{perl5_corelib}/IPC/Cmd.pm
%attr(0444,root,root) %{perl5_corelib}/IPC/Open2.pm
%attr(0444,root,root) %{perl5_corelib}/IPC/Open3.pm
# Internals.pod
%attr(0444,root,root) %{perl5_corelib}/Internals.pod
# JSON
%dir %{perl5_corelib}/JSON
%attr(0444,root,root) %{perl5_corelib}/JSON/PP.pm
%dir %{perl5_corelib}/JSON/PP
%attr(0444,root,root) %{perl5_corelib}/JSON/PP/Boolean.pm
# List
%dir %{perl5_corearch}/List
%attr(0444,root,root) %{perl5_corearch}/List/Util.pm
%dir %{perl5_corearch}/List/Util
%attr(0444,root,root) %{perl5_corearch}/List/Util/XS.pm
%dir %{perl5_corearch}/auto/List
%dir %{perl5_corearch}/auto/List/Util
%attr(0555,root,root) %{perl5_corearch}/auto/List/Util/Util.so
# Locale
%dir %{perl5_corelib}/Locale
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext.pm
%dir %{perl5_corelib}/Locale/Maketext
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext/Cookbook.pod
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext/Guts.pm
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext/GutsLoader.pm
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext/Simple.pm
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext/TPJ13.pod
%attr(0444,root,root) %{perl5_corelib}/Locale/Maketext.pod
# MIME
%dir %{perl5_corearch}/MIME
%attr(0444,root,root) %{perl5_corearch}/MIME/Base64.pm
%attr(0444,root,root) %{perl5_corearch}/MIME/QuotedPrint.pm
%dir %{perl5_corearch}/auto/MIME
%dir %{perl5_corearch}/auto/MIME/Base64
%attr(0555,root,root) %{perl5_corearch}/auto/MIME/Base64/Base64.so
# Math
%dir %{perl5_corearch}/Math
%dir %{perl5_corearch}/Math/BigInt
%attr(0444,root,root) %{perl5_corearch}/Math/BigInt/FastCalc.pm
%dir %{perl5_corearch}/auto/Math
%dir %{perl5_corearch}/auto/Math/BigInt
%dir %{perl5_corearch}/auto/Math/BigInt/FastCalc
%attr(0555,root,root) %{perl5_corearch}/auto/Math/BigInt/FastCalc/FastCalc.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Math
%dir %{perl5_corelib}/Math/BigInt
%endif
%attr(0444,root,root) %{perl5_corelib}/Math/BigFloat.pm
%dir %{perl5_corelib}/Math/BigFloat
%attr(0444,root,root) %{perl5_corelib}/Math/BigFloat/Trace.pm
%attr(0444,root,root) %{perl5_corelib}/Math/BigInt.pm
%attr(0444,root,root) %{perl5_corelib}/Math/BigInt/Calc.pm
%attr(0444,root,root) %{perl5_corelib}/Math/BigInt/Lib.pm
%attr(0444,root,root) %{perl5_corelib}/Math/BigInt/Trace.pm
%attr(0444,root,root) %{perl5_corelib}/Math/BigRat.pm
%dir %{perl5_corelib}/Math/BigRat
%attr(0444,root,root) %{perl5_corelib}/Math/BigRat/Trace.pm
%attr(0444,root,root) %{perl5_corelib}/Math/Complex.pm
%attr(0444,root,root) %{perl5_corelib}/Math/Trig.pm
# Memoize
%attr(0444,root,root) %{perl5_corelib}/Memoize.pm
%dir %{perl5_corelib}/Memoize
%attr(0444,root,root) %{perl5_corelib}/Memoize/AnyDBM_File.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/Expire.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/ExpireFile.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/ExpireTest.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/NDBM_File.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/SDBM_File.pm
%attr(0444,root,root) %{perl5_corelib}/Memoize/Storable.pm
# Module
%dir %{perl5_corelib}/Module
%attr(0444,root,root) %{perl5_corelib}/Module/CoreList.pm
%dir %{perl5_corelib}/Module/CoreList
%attr(0444,root,root) %{perl5_corelib}/Module/CoreList/Utils.pm
%attr(0444,root,root) %{perl5_corelib}/Module/CoreList.pod
%attr(0444,root,root) %{perl5_corelib}/Module/Load.pm
%dir %{perl5_corelib}/Module/Load
%attr(0444,root,root) %{perl5_corelib}/Module/Load/Conditional.pm
%attr(0444,root,root) %{perl5_corelib}/Module/Loaded.pm
%attr(0444,root,root) %{perl5_corelib}/Module/Metadata.pm
# NDBM_File
%attr(0444,root,root) %{perl5_corearch}/NDBM_File.pm
%dir %{perl5_corearch}/auto/NDBM_File
%attr(0555,root,root) %{perl5_corearch}/auto/NDBM_File/NDBM_File.so
# NEXT.pm
%attr(0444,root,root) %{perl5_corelib}/NEXT.pm
# Net
%dir %{perl5_corelib}/Net
%attr(0444,root,root) %{perl5_corelib}/Net/*.pm
%attr(0444,root,root) %{perl5_corelib}/Net/libnetFAQ.pod
%dir %{perl5_corelib}/Net/FTP
%attr(0444,root,root) %{perl5_corelib}/Net/FTP/*.pm
# O
%attr(0444,root,root) %{perl5_corearch}/O.pm
# ODBM_FILE
%attr(0444,root,root) %{perl5_corearch}/ODBM_File.pm
%dir %{perl5_corearch}/auto/ODBM_File
%attr(0555,root,root) %{perl5_corearch}/auto/ODBM_File/ODBM_File.so
# Opcode
%attr(0444,root,root) %{perl5_corearch}/Opcode.pm
%dir %{perl5_corearch}/auto/Opcode
%attr(0555,root,root) %{perl5_corearch}/auto/Opcode/Opcode.so
# POSIX
%attr(0444,root,root) %{perl5_corearch}/POSIX.pm
%attr(0444,root,root) %{perl5_corearch}/POSIX.pod
%dir %{perl5_corearch}/auto/POSIX
%attr(0444,root,root) %{perl5_corearch}/auto/POSIX/POSIX.so
# Params
%dir %{perl5_corelib}/Params
%attr(0444,root,root) %{perl5_corelib}/Params/Check.pm
# Parse
%dir %{perl5_corelib}/Parse
%dir %{perl5_corelib}/Parse/CPAN
%attr(0444,root,root) %{perl5_corelib}/Parse/CPAN/Meta.pm
# Perl
%dir %{perl5_corelib}/Perl
%attr(0444,root,root) %{perl5_corelib}/Perl/OSType.pm
# PerlIO
%dir %{perl5_corearch}/PerlIO
%attr(0444,root,root) %{perl5_corearch}/PerlIO/encoding.pm
%attr(0444,root,root) %{perl5_corearch}/PerlIO/mmap.pm
%attr(0444,root,root) %{perl5_corearch}/PerlIO/scalar.pm
%attr(0444,root,root) %{perl5_corearch}/PerlIO/via.pm
%dir %{perl5_corearch}/auto/PerlIO
%dir %{perl5_corearch}/auto/PerlIO/encoding
%attr(0555,root,root) %{perl5_corearch}/auto/PerlIO/encoding/encoding.so
%dir %{perl5_corearch}/auto/PerlIO/mmap
%attr(0555,root,root) %{perl5_corearch}/auto/PerlIO/mmap/mmap.so
%dir %{perl5_corearch}/auto/PerlIO/scalar
%attr(0555,root,root) %{perl5_corearch}/auto/PerlIO/scalar/scalar.so
%dir %{perl5_corearch}/auto/PerlIO/via
%attr(0555,root,root) %{perl5_corearch}/auto/PerlIO/via/via.so
%attr(0444,root,root) %{perl5_corelib}/PerlIO.pm
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/PerlIO
%endif
%dir %{perl5_corelib}/PerlIO/via
%attr(0444,root,root) %{perl5_corelib}/PerlIO/via/QuotedPrint.pm
# Pod
%dir %{perl5_corelib}/Pod
%attr(0444,root,root) %{perl5_corelib}/Pod/Checker.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Escapes.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Functions.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Html.pm
%dir %{perl5_corelib}/Pod/Html
%attr(0444,root,root) %{perl5_corelib}/Pod/Html/Util.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Man.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/ParseLink.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Perldoc.pm
%dir %{perl5_corelib}/Pod/Perldoc
%attr(0444,root,root) %{perl5_corelib}/Pod/Perldoc/*.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Simple.pm
%dir %{perl5_corelib}/Pod/Simple
%attr(0444,root,root) %{perl5_corelib}/Pod/Simple/*.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Simple/Subclassing.pod
%attr(0444,root,root) %{perl5_corelib}/Pod/Simple.pod
%attr(0444,root,root) %{perl5_corelib}/Pod/Text.pm
%dir %{perl5_corelib}/Pod/Text
%attr(0444,root,root) %{perl5_corelib}/Pod/Text/Color.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Text/Overstrike.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Text/Termcap.pm
%attr(0444,root,root) %{perl5_corelib}/Pod/Usage.pm
# SDBM_File
%attr(0444,root,root) %{perl5_corearch}/SDBM_File.pm
%dir %{perl5_corearch}/auto/SDBM_File
%attr(0555,root,root) %{perl5_corearch}/auto/SDBM_File/SDBM_File.so
# Safe.pm
%attr(0444,root,root) %{perl5_corelib}/Safe.pm
# Scalar
%dir %{perl5_corearch}/Scalar
%attr(0444,root,root) %{perl5_corearch}/Scalar/Util.pm
# Search
%dir %{perl5_corelib}/Search
%attr(0444,root,root) %{perl5_corelib}/Search/Dict.pm
# SelectSaver.pm -- SelfLoader.pm
%attr(0444,root,root) %{perl5_corelib}/SelectSaver.pm
%attr(0444,root,root) %{perl5_corelib}/SelfLoader.pm
# Socket
%attr(0444,root,root) %{perl5_corearch}/Socket.pm
%dir %{perl5_corearch}/auto/Socket
%attr(0555,root,root) %{perl5_corearch}/auto/Socket/Socket.so
# Storable
%attr(0444,root,root) %{perl5_corearch}/Storable.pm
%dir %{perl5_corearch}/auto/Storable
%attr(0555,root,root) %{perl5_corearch}/auto/Storable/Storable.so
# Sub
%dir %{perl5_corearch}/Sub
%attr(0444,root,root) %{perl5_corearch}/Sub/Util.pm
# Symbol.pm
%attr(0444,root,root) %{perl5_corelib}/Symbol.pm
# Sys
%dir %{perl5_corearch}/Sys
%attr(0444,root,root) %{perl5_corearch}/Sys/Hostname.pm
%attr(0444,root,root) %{perl5_corearch}/Sys/Syslog.pm
%dir %{perl5_corearch}/auto/Sys/Hostname
%attr(0555,root,root) %{perl5_corearch}/auto/Sys/Hostname/Hostname.so
%dir %{perl5_corearch}/auto/Sys/Syslog
%attr(0555,root,root) %{perl5_corearch}/auto/Sys/Syslog/Syslog.so
# TAP
%dir %{perl5_corelib}/TAP
%attr(0444,root,root) %{perl5_corelib}/TAP/Base.pm
%dir %{perl5_corelib}/TAP/Formatter
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Base.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Color.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Console.pm
%dir %{perl5_corelib}/TAP/Formatter/Console
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Console/ParallelSession.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Console/Session.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/File.pm
%dir %{perl5_corelib}/TAP/Formatter/File
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/File/Session.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Formatter/Session.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Harness.pm
%dir %{perl5_corelib}/TAP/Harness
%attr(0444,root,root) %{perl5_corelib}/TAP/Harness/Beyond.pod
%attr(0444,root,root) %{perl5_corelib}/TAP/Harness/Env.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Object.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser.pm
%dir %{perl5_corelib}/TAP/Parser
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Aggregator.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Grammar.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Iterator.pm
%dir %{perl5_corelib}/TAP/Parser/Iterator
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Iterator/Array.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Iterator/Process.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Iterator/Stream.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/IteratorFactory.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Multiplexer.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result.pm
%dir %{perl5_corelib}/TAP/Parser/Result
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Bailout.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Comment.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Plan.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Pragma.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Test.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Unknown.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/Version.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Result/YAML.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/ResultFactory.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Scheduler.pm
%dir %{perl5_corelib}/TAP/Parser/Scheduler
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Scheduler/Job.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Scheduler/Spinner.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/Source.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler.pm
%dir %{perl5_corelib}/TAP/Parser/SourceHandler
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler/Executable.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler/File.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler/Handle.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler/Perl.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/SourceHandler/RawTAP.pm
%dir %{perl5_corelib}/TAP/Parser/YAMLish
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/YAMLish/Reader.pm
%attr(0444,root,root) %{perl5_corelib}/TAP/Parser/YAMLish/Writer.pm
#term
%dir %{perl5_corelib}/Term
%attr(0444,root,root) %{perl5_corelib}/Term/ANSIColor.pm
%attr(0444,root,root) %{perl5_corelib}/Term/Cap.pm
%attr(0444,root,root) %{perl5_corelib}/Term/Complete.pm
%attr(0444,root,root) %{perl5_corelib}/Term/ReadLine.pm
# Test
%attr(0444,root,root) %{perl5_corelib}/Test.pm
%dir %{perl5_corelib}/Test
%attr(0444,root,root) %{perl5_corelib}/Test/Builder.pm
%dir %{perl5_corelib}/Test/Builder
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/Formatter.pm
%dir %{perl5_corelib}/Test/Builder/IO
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/IO/Scalar.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/Module.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/Tester.pm
%dir %{perl5_corelib}/Test/Builder/Tester
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/Tester/Color.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Builder/TodoDiag.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Harness.pm
%attr(0444,root,root) %{perl5_corelib}/Test/More.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Simple.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Tester.pm
%dir %{perl5_corelib}/Test/Tester
%attr(0444,root,root) %{perl5_corelib}/Test/Tester/Capture.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Tester/CaptureRunner.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Tester/Delegate.pm
%attr(0444,root,root) %{perl5_corelib}/Test/Tutorial.pod
%dir %{perl5_corelib}/Test/use
%attr(0444,root,root) %{perl5_corelib}/Test/use/ok.pm
# Test2
%attr(0444,root,root) %{perl5_corelib}/Test2.pm
%dir %{perl5_corelib}/Test2
%attr(0444,root,root) %{perl5_corelib}/Test2/API.pm
%dir %{perl5_corelib}/Test2/API
%attr(0444,root,root) %{perl5_corelib}/Test2/API/Breakage.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/Context.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/Instance.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/InterceptResult.pm
%dir %{perl5_corelib}/Test2/API/InterceptResult
%attr(0444,root,root) %{perl5_corelib}/Test2/API/InterceptResult/Event.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/InterceptResult/Facet.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/InterceptResult/Hub.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/InterceptResult/Squasher.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/API/Stack.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event.pm
%dir %{perl5_corelib}/Test2/Event
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Bail.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Diag.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Encoding.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Exception.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Fail.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Generic.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Note.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Ok.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Pass.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Plan.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Skip.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Subtest.pm
%dir %{perl5_corelib}/Test2/Event/TAP
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/TAP/Version.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/V2.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Event/Waiting.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet.pm
%dir %{perl5_corelib}/Test2/EventFacet
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/About.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Amnesty.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Assert.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Control.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Error.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Hub.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Info.pm
%dir %{perl5_corelib}/Test2/EventFacet/Info
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Info/Table.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Meta.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Parent.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Plan.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Render.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/EventFacet/Trace.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Formatter.pm
%dir %{perl5_corelib}/Test2/Formatter
%attr(0444,root,root) %{perl5_corelib}/Test2/Formatter/TAP.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Hub.pm
%dir %{perl5_corelib}/Test2/Hub
%attr(0444,root,root) %{perl5_corelib}/Test2/Hub/Interceptor.pm
%dir %{perl5_corelib}/Test2/Hub/Interceptor
%attr(0444,root,root) %{perl5_corelib}/Test2/Hub/Interceptor/Terminator.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Hub/Subtest.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/IPC.pm
%dir %{perl5_corelib}/Test2/IPC
%attr(0444,root,root) %{perl5_corelib}/Test2/IPC/Driver.pm
%dir %{perl5_corelib}/Test2/IPC/Driver
%attr(0444,root,root) %{perl5_corelib}/Test2/IPC/Driver/Files.pm
%dir %{perl5_corelib}/Test2/Tools
%attr(0444,root,root) %{perl5_corelib}/Test2/Tools/Tiny.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Transition.pod
%attr(0444,root,root) %{perl5_corelib}/Test2/Util.pm
%dir %{perl5_corelib}/Test2/Util
%attr(0444,root,root) %{perl5_corelib}/Test2/Util/ExternalMeta.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Util/Facets2Legacy.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Util/HashBase.pm
%attr(0444,root,root) %{perl5_corelib}/Test2/Util/Trace.pm
# Text
%dir %{perl5_corelib}/Text
%attr(0444,root,root) %{perl5_corelib}/Text/Abbrev.pm
%attr(0444,root,root) %{perl5_corelib}/Text/Balanced.pm
%attr(0444,root,root) %{perl5_corelib}/Text/ParseWords.pm
%attr(0444,root,root) %{perl5_corelib}/Text/Tabs.pm
%attr(0444,root,root) %{perl5_corelib}/Text/Wrap.pm
# Thread
%attr(0444,root,root) %{perl5_corelib}/Thread.pm
%dir %{perl5_corelib}/Thread
%attr(0444,root,root) %{perl5_corelib}/Thread/Queue.pm
%attr(0444,root,root) %{perl5_corelib}/Thread/Semaphore.pm
# Tie
%dir %{perl5_corelib}/Tie
%attr(0444,root,root) %{perl5_corelib}/Tie/Array.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/File.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/Handle.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/Hash.pm
%dir %{perl5_corelib}/Tie/Hash
%attr(0444,root,root) %{perl5_corelib}/Tie/Hash/NamedCapture.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/Memoize.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/RefHash.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/Scalar.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/StdHandle.pm
%attr(0444,root,root) %{perl5_corelib}/Tie/SubstrHash.pm
# Time
%dir %{perl5_corearch}/Time
%attr(0444,root,root) %{perl5_corearch}/Time/HiRes.pm
%attr(0444,root,root) %{perl5_corearch}/Time/Piece.pm
%attr(0444,root,root) %{perl5_corearch}/Time/Seconds.pm
%dir %{perl5_corearch}/auto/Time
%dir %{perl5_corearch}/auto/Time/HiRes
%attr(0555,root,root) %{perl5_corearch}/auto/Time/HiRes/HiRes.so
%dir %{perl5_corearch}/auto/Time/Piece
%attr(0555,root,root) %{perl5_corearch}/auto/Time/Piece/Piece.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Time
%endif
%attr(0444,root,root) %{perl5_corelib}/Time/Local.pm
%attr(0444,root,root) %{perl5_corelib}/Time/gmtime.pm
%attr(0444,root,root) %{perl5_corelib}/Time/localtime.pm
%attr(0444,root,root) %{perl5_corelib}/Time/tm.pm
# UNIVERSAL.pm
%attr(0444,root,root) %{perl5_corelib}/UNIVERSAL.pm
# Unicode
%dir %{perl5_corearch}/Unicode
%attr(0444,root,root) %{perl5_corearch}/Unicode/Collate.pm
%dir %{perl5_corearch}/Unicode/Collate
%attr(0444,root,root) %{perl5_corearch}/Unicode/Collate/Locale.pm
%attr(0444,root,root) %{perl5_corearch}/Unicode/Normalize.pm
%dir %{perl5_corearch}/auto/Unicode
%dir %{perl5_corearch}/auto/Unicode/Collate
%attr(0555,root,root) %{perl5_corearch}/auto/Unicode/Collate/Collate.so
%dir %{perl5_corearch}/auto/Unicode/Normalize
%attr(0555,root,root) %{perl5_corearch}/auto/Unicode/Normalize/Normalize.so
%if 0%{?linuxMultiarch:1} == 1
%dir %{perl5_corelib}/Unicode
%dir %{perl5_corelib}/Unicode/Collate
%endif
%dir %{perl5_corelib}/Unicode/Collate/CJK
%attr(0444,root,root) %{perl5_corelib}/Unicode/Collate/CJK/*.pm
%dir %{perl5_corelib}/Unicode/Collate/Locale
%attr(0444,root,root) %{perl5_corelib}/Unicode/Collate/Locale/*.pl
%attr(0444,root,root) %{perl5_corelib}/Unicode/Collate/allkeys.txt
%attr(0444,root,root) %{perl5_corelib}/Unicode/Collate/keys.txt
%attr(0444,root,root) %{perl5_corelib}/Unicode/UCD.pm
# User
%dir %{perl5_corelib}/User
%attr(0444,root,root) %{perl5_corelib}/User/grent.pm
%attr(0444,root,root) %{perl5_corelib}/User/pwent.pm
# XSLoader.pm -- _charnames.pm
%attr(0444,root,root) %{perl5_corelib}/XSLoader.pm
%attr(0444,root,root) %{perl5_corelib}/_charnames.pm
# attributes
%attr(0444,root,root) %{perl5_corearch}/attributes.pm
%dir %{perl5_corearch}/auto/attributes
%attr(0555,root,root) %{perl5_corearch}/auto/attributes/attributes.so
# autodie
%attr(0444,root,root) %{perl5_corelib}/autodie.pm
%dir %{perl5_corelib}/autodie
%dir %{perl5_corelib}/autodie/Scope
%attr(0444,root,root) %{perl5_corelib}/autodie/Scope/Guard.pm
%attr(0444,root,root) %{perl5_corelib}/autodie/Scope/GuardStack.pm
%attr(0444,root,root) %{perl5_corelib}/autodie/Util.pm
%attr(0444,root,root) %{perl5_corelib}/autodie/exception.pm
%dir %{perl5_corelib}/autodie/exception
%attr(0444,root,root) %{perl5_corelib}/autodie/exception/system.pm
%attr(0444,root,root) %{perl5_corelib}/autodie/hints.pm
%attr(0444,root,root) %{perl5_corelib}/autodie/skip.pm
# autouse.pm -- dumpvar.pl
%attr(0444,root,root) %{perl5_corelib}/autouse.pm
%attr(0444,root,root) %{perl5_corelib}/base.pm
%attr(0444,root,root) %{perl5_corelib}/bigfloat.pm
%attr(0444,root,root) %{perl5_corelib}/bigint.pm
%attr(0444,root,root) %{perl5_corelib}/bignum.pm
%attr(0444,root,root) %{perl5_corelib}/bigrat.pm
%attr(0444,root,root) %{perl5_corelib}/blib.pm
%attr(0444,root,root) %{perl5_corelib}/builtin.pm
%attr(0444,root,root) %{perl5_corelib}/bytes.pm
%attr(0444,root,root) %{perl5_corelib}/bytes_heavy.pl
%attr(0444,root,root) %{perl5_corelib}/charnames.pm
%attr(0444,root,root) %{perl5_corelib}/constant.pm
%attr(0444,root,root) %{perl5_corelib}/deprecate.pm
%attr(0444,root,root) %{perl5_corelib}/diagnostics.pm
%attr(0444,root,root) %{perl5_corelib}/dumpvar.pl
# encoding
%attr(0444,root,root) %{perl5_corearch}/encoding.pm
%dir %{perl5_corelib}/encoding
%attr(0444,root,root) %{perl5_corelib}/encoding/warnings.pm
# experimental.pm -- less.pm
%attr(0444,root,root) %{perl5_corelib}/experimental.pm
%attr(0444,root,root) %{perl5_corelib}/feature.pm
%attr(0444,root,root) %{perl5_corelib}/fields.pm
%attr(0444,root,root) %{perl5_corelib}/filetest.pm
%attr(0444,root,root) %{perl5_corelib}/if.pm
%attr(0444,root,root) %{perl5_corelib}/integer.pm
%attr(0444,root,root) %{perl5_corelib}/less.pm
# lib
%attr(0444,root,root) %{perl5_corearch}/lib.pm
# locale.pm
%attr(0444,root,root) %{perl5_corelib}/locale.pm
# meta_notation.pm
%attr(0444,root,root) %{perl5_corelib}/meta_notation.pm
# mro
%attr(0444,root,root) %{perl5_corearch}/mro.pm
%dir %{perl5_corearch}/auto/mro
%attr(0555,root,root) %{perl5_corearch}/auto/mro/mro.so
# ok.pm
%attr(0444,root,root) %{perl5_corelib}/ok.pm
# open.pm
%attr(0444,root,root) %{perl5_corelib}/open.pm
# ops
%attr(0444,root,root) %{perl5_corearch}/ops.pm
# overload
%attr(0444,root,root) %{perl5_corelib}/overload.pm
%dir %{perl5_corelib}/overload
%attr(0444,root,root) %{perl5_corelib}/overload/numbers.pm
%attr(0444,root,root) %{perl5_corelib}/overloading.pm
# parent.pm
%attr(0444,root,root) %{perl5_corelib}/parent.pm
# perl5db.pl
%attr(0444,root,root) %{perl5_corelib}/perl5db.pl
# perlfaq.pm
%attr(0444,root,root) %{perl5_corelib}/perlfaq.pm
# re
%attr(0444,root,root) %{perl5_corearch}/re.pm
%dir %{perl5_corearch}/auto/re
%attr(0555,root,root) %{perl5_corearch}/auto/re/re.so
# sigtrap.pm
%attr(0444,root,root) %{perl5_corelib}/sigtrap.pm
# sort.pm
%attr(0444,root,root) %{perl5_corelib}/sort.pm
# strict.pm
%attr(0444,root,root) %{perl5_corelib}/strict.pm
# subs.pm
%attr(0444,root,root) %{perl5_corelib}/subs.pm
# threads
%attr(0444,root,root) %{perl5_corearch}/threads.pm
%dir %{perl5_corearch}/threads
%attr(0444,root,root) %{perl5_corearch}/threads/shared.pm
%dir %{perl5_corearch}/auto/threads
%attr(0555,root,root) %{perl5_corearch}/auto/threads/threads.so
%dir %{perl5_corearch}/auto/threads/shared
%attr(0555,root,root) %{perl5_corearch}/auto/threads/shared/shared.so
# unicore
%dir %{perl5_corelib}/unicore
%attr(0444,root,root) %{perl5_corelib}/unicore/Blocks.txt
%attr(0444,root,root) %{perl5_corelib}/unicore/CombiningClass.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/Decomposition.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/Name.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/Name.pm
%attr(0444,root,root) %{perl5_corelib}/unicore/NamedSequences.txt
%attr(0444,root,root) %{perl5_corelib}/unicore/SpecialCasing.txt
%attr(0444,root,root) %{perl5_corelib}/unicore/UCD.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/uni_keywords.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/version
%dir %{perl5_corelib}/unicore/To
%attr(0444,root,root) %{perl5_corelib}/unicore/To/*.pl
%dir %{perl5_corelib}/unicore/lib
%dir %{perl5_corelib}/unicore/lib/Age
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Age/*.pl
%dir %{perl5_corelib}/unicore/lib/Alpha
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Alpha/Y.pl
%dir %{perl5_corelib}/unicore/lib/Bc
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Bc/*.pl
%dir %{perl5_corelib}/unicore/lib/BidiC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/BidiC/Y.pl
%dir %{perl5_corelib}/unicore/lib/BidiM
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/BidiM/Y.pl
%dir %{perl5_corelib}/unicore/lib/Blk
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Blk/NB.pl
%dir %{perl5_corelib}/unicore/lib/Bpt
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Bpt/*.pl
%dir %{perl5_corelib}/unicore/lib/CE
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CE/Y.pl
%dir %{perl5_corelib}/unicore/lib/CI
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CI/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWCF
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWCF/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWCM
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWCM/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWKCF
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWKCF/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWL
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWL/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWT
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWT/Y.pl
%dir %{perl5_corelib}/unicore/lib/CWU
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CWU/Y.pl
%dir %{perl5_corelib}/unicore/lib/Cased
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Cased/Y.pl
%dir %{perl5_corelib}/unicore/lib/Ccc
%attr(0644,root,root) %{perl5_corelib}/unicore/lib/Ccc/*.pl
%dir %{perl5_corelib}/unicore/lib/CompEx
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/CompEx/Y.pl
%dir %{perl5_corelib}/unicore/lib/DI
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/DI/Y.pl
%dir %{perl5_corelib}/unicore/lib/Dash
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Dash/Y.pl
%dir %{perl5_corelib}/unicore/lib/Dep
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Dep/Y.pl
%dir %{perl5_corelib}/unicore/lib/Dia
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Dia/Y.pl
%dir %{perl5_corelib}/unicore/lib/Dt
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Dt/*.pl
%dir %{perl5_corelib}/unicore/lib/EBase
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/EBase/Y.pl
%dir %{perl5_corelib}/unicore/lib/EComp
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/EComp/Y.pl
%dir %{perl5_corelib}/unicore/lib/EPres
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/EPres/Y.pl
%dir %{perl5_corelib}/unicore/lib/Ea
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Ea/*.pl
%dir %{perl5_corelib}/unicore/lib/Emoji
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Emoji/Y.pl
%dir %{perl5_corelib}/unicore/lib/Ext
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Ext/Y.pl
%dir %{perl5_corelib}/unicore/lib/ExtPict
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/ExtPict/Y.pl
%dir %{perl5_corelib}/unicore/lib/GCB
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/GCB/*.pl
%dir %{perl5_corelib}/unicore/lib/Gc
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Gc/*.pl
%dir %{perl5_corelib}/unicore/lib/GrBase
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/GrBase/Y.pl
%dir %{perl5_corelib}/unicore/lib/GrExt
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/GrExt/Y.pl
%dir %{perl5_corelib}/unicore/lib/Hex
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Hex/Y.pl
%dir %{perl5_corelib}/unicore/lib/Hst
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Hst/NA.pl
%dir %{perl5_corelib}/unicore/lib/Hyphen
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Hyphen/T.pl
%dir %{perl5_corelib}/unicore/lib/IDC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/IDC/Y.pl
%dir %{perl5_corelib}/unicore/lib/IDS
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/IDS/Y.pl
%dir %{perl5_corelib}/unicore/lib/IdStatus
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/IdStatus/Allowed.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/IdStatus/Restrict.pl
%dir %{perl5_corelib}/unicore/lib/IdType
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/IdType/*.pl
%dir %{perl5_corelib}/unicore/lib/Ideo
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Ideo/Y.pl
%dir %{perl5_corelib}/unicore/lib/In
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/In/*.pl
%dir %{perl5_corelib}/unicore/lib/InPC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/InPC/*.pl
%dir %{perl5_corelib}/unicore/lib/InSC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/InSC/*.pl
%dir %{perl5_corelib}/unicore/lib/Jg
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Jg/*.pl
%dir %{perl5_corelib}/unicore/lib/Jt
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Jt/*.pl
%dir %{perl5_corelib}/unicore/lib/Lb
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Lb/*.pl
%dir %{perl5_corelib}/unicore/lib/Lower
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Lower/Y.pl
%dir %{perl5_corelib}/unicore/lib/Math
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Math/Y.pl
%dir %{perl5_corelib}/unicore/lib/NFCQC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFCQC/M.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFCQC/Y.pl
%dir %{perl5_corelib}/unicore/lib/NFDQC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFDQC/N.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFDQC/Y.pl
%dir %{perl5_corelib}/unicore/lib/NFKCQC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFKCQC/N.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFKCQC/Y.pl
%dir %{perl5_corelib}/unicore/lib/NFKDQC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFKDQC/N.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/NFKDQC/Y.pl
%dir %{perl5_corelib}/unicore/lib/Nt
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Nt/Di.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Nt/None.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Nt/Nu.pl
%dir %{perl5_corelib}/unicore/lib/Nv
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Nv/*.pl
%dir %{perl5_corelib}/unicore/lib/PCM
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/PCM/Y.pl
%dir %{perl5_corelib}/unicore/lib/PatSyn
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/PatSyn/Y.pl
%dir %{perl5_corelib}/unicore/lib/Perl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Perl/*.pl
%dir %{perl5_corelib}/unicore/lib/QMark
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/QMark/Y.pl
%dir %{perl5_corelib}/unicore/lib/SB
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/SB/*.pl
%dir %{perl5_corelib}/unicore/lib/SD
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/SD/Y.pl
%dir %{perl5_corelib}/unicore/lib/STerm
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/STerm/Y.pl
%dir %{perl5_corelib}/unicore/lib/Sc
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Sc/*.pl
%dir %{perl5_corelib}/unicore/lib/Scx
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Scx/*.pl
%dir %{perl5_corelib}/unicore/lib/Term
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Term/Y.pl
%dir %{perl5_corelib}/unicore/lib/UIdeo
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/UIdeo/Y.pl
%dir %{perl5_corelib}/unicore/lib/Upper
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Upper/Y.pl
%dir %{perl5_corelib}/unicore/lib/VS
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/VS/Y.pl
%dir %{perl5_corelib}/unicore/lib/Vo
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Vo/R.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Vo/Tr.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Vo/Tu.pl
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/Vo/U.pl
%dir %{perl5_corelib}/unicore/lib/WB
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/WB/*.pl
%dir %{perl5_corelib}/unicore/lib/XIDC
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/XIDC/Y.pl
%dir %{perl5_corelib}/unicore/lib/XIDS
%attr(0444,root,root) %{perl5_corelib}/unicore/lib/XIDS/Y.pl
# utf8
%attr(0444,root,root) %{perl5_corelib}/utf8.pm
# vars
%attr(0444,root,root) %{perl5_corelib}/vars.pm
# version
%attr(0444,root,root) %{perl5_corelib}/version.pm
%attr(0444,root,root) %{perl5_corelib}/version.pod
%dir %{perl5_corelib}/version
%attr(0444,root,root) %{perl5_corelib}/version/Internals.pod
%attr(0444,root,root) %{perl5_corelib}/version/regex.pm
# vmsish
%attr(0444,root,root) %{perl5_corelib}/vmsish.pm
# warnings
%attr(0444,root,root) %{perl5_corelib}/warnings.pm
%dir %{perl5_corelib}/warnings
%attr(0444,root,root) %{perl5_corelib}/warnings/register.pm
#
# ???
%exclude %{perl5_corearch}/.packlist
#
# pod - may need refinement
%dir %{perl5_corelib}/pod
%attr(0644,root,root) %{perl5_corelib}/pod/*.pod
#man pages
#%%{_mandir}/man1/*.1*
#%%{_mandir}/man3/*.3*
%license Artistic Copying README
%doc %{name}-make.test.log
%doc Artistic Copying AUTHORS README README.linux

%files devel
%defattr(-,root,root)
%attr(0644,root,root) /usr/lib/rpm/macros.d/macros.perl
%attr(0755,root,root) %{_bindir}/h2xs
%attr(0755,root,root) %{_bindir}/perlivp
#CORE
%dir %{perl5_corearch}/CORE
%attr(0444,root,root) %{perl5_corearch}/CORE/*.h
# man pages
%{_mandir}/man1/h2xs.1*
%{_mandir}/man1/perlivp.1*
%license Artistic Copying README
%doc Artistic Copying README

%files libperl
%defattr(-,root,root,-)
%attr(0555,root,root) %{perl5_corearch}/CORE/libperl.so
%license Artistic Copying README
%doc Artistic Copying README

##########################
#                        #
# Separable Perl Modules #
#                        #
##########################

%files Digest-MD5
%defattr(-,root,root,-)
%dir %{perl5_corearch}/Digest
%attr(0444,root,root) %{perl5_corearch}/Digest/MD5.pm
%dir %{perl5_corearch}/auto/Digest
%dir %{perl5_corearch}/auto/Digest/MD5
%attr(0555,root,root) %{perl5_corearch}/auto/Digest/MD5/MD5.so
%attr(0644,root,root) %{_mandir}/man3/Digest::MD5.3*
%license Artistic Copying README
%doc Artistic Copying README

%files Digest-SHA
%defattr(-,root,root,-)
%dir %{perl5_corearch}/Digest
%attr(0444,root,root) %{perl5_corearch}/Digest/SHA.pm
%dir %{perl5_corearch}/auto/Digest
%dir %{perl5_corearch}/auto/Digest/SHA
%attr(0555,root,root) %{perl5_corearch}/auto/Digest/SHA/SHA.so
%attr(0644,root,root) %{_mandir}/man3/Digest::SHA.3*

%changelog
* Tue Apr 25 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.1-0.dev9
- Changed core RPM macros

* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.1-0.dev8
- Working on subpackages

* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.1-0.dev7
- Update to 5.36.1

* Sun Apr 23 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev6
- Started work on subpackages

* Sat Apr 22 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev5
- New API/ABI macros, remove subpackage for Perl 5 licenses (doing
- that differently)

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev4
- Add subpackage for the Perl 5 licenses

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev2
- Fix packaging bug (wrong perms on a few directories), filter out
-  bogus requires, enable stripping.

* Thu Apr 20 2023 Michael A. Peters <anymouseprophet@gmail.com> - 2:5.36.0-0.dev1
- Initial spec file for YJL (RPM bootstrapping LFS/BLFS 11.3)
