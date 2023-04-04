# /etc/profile.d/texlive.sh - set *PATH variables for TeXLive

checkuser () {
  ### returns 0 only for non-root members of texlive group
  if [ "`id -u`" == "0" ]; then
    return 1
  fi
  TLGID="`id -g texlive`" 2> /dev/null
  if [ $? -ne 0 ]; then
    return 1
  fi
  for id in `id -G`; do
    if [ "${id}" == "${TLGID}" ]; then
      return 0
    fi
  done
  return 1
}

tlversion () {
  ### returns 0 only if it finds an ls-R in texmf-dist
  ### only checks for versions within last seven years.
  YYYY=`date +%Y`
  for n in 0 1 2 3 4 5 6 7; do
    DIR="`echo "${YYYY} - ${n}" |bc`"
    if [ -f /opt/texlive/${DIR}/texmf-dist/ls-R ]; then
      printf ${DIR}
      return 0
    fi
  done
  return 1
}

tlplatform () {
  HARDWARE="`uname -m`"
  OS="`uname -o`"
  case "${OS}" in
    GNU/Linux)
      case "${HARDWARE}" in
        x86_64)
          printf "x86_64-linux"
          ;;
        arm64)
          printf "aarch64-linux"
          ;;
        i386 | i486 | i586 | i686)
          printf "i386-linux"
          ;;
        *)
          # hardware not (yet) supported by script
          return 1
          ;;
      esac
      ;;
    *)
      # OS not (yet) supported by script
      return 1
      ;;
  esac
  return 0
}

if checkuser; then
  TLPLATFORM="`tlplatform`"
  if [ $? -eq 0 ]; then
    TLIVEV="`tlversion`"
    if [ $? -eq 0 ]; then
      # pathprepend/pathappend defined in BLFS/YJL /etc/profile
      pathprepend /opt/texlive/${TLIVEV}/bin/${TLPLATFORM}
      # make sure these two are first
      pathprepend /usr/bin
      pathprepend /usr/local/bin
      # man/info
      pathappend /opt/texlive/${TLIVEV}/texmf-dist/doc/info INFOPATH
      pathappend /opt/texlive/${TLIVEV}/texmf-dist/doc/man MANPATH
    fi
  fi
fi

# End /etc/profile.d/texlive.sh
