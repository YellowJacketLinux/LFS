#!/bin/bash

# set umask
umask 022

if [ "`id -un`" != "texlive" ]; then
  echo "This script can only be executed by the texlive administrative user."
  echo "To become that user from an administrative account:"
  echo ""
  echo "sudo su - texlive"
  exit 1
fi

TMPDIR="`mktemp --tmpdir -d tlive-XXXXXXXXXXXX`" > /dev/null 2>&1

trap "rm -rf ${TMPDIR}" EXIT TERM

pushd ${TMPDIR} > /dev/null 2>&1

/usr/bin/curl -L -O https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
if [ $? -ne 0 ]; then
  echo "Aborting. Can not download installer."
  exit 1
fi
tar -zxf install-tl-unx.tar.gz
if [ $? -ne 0 ]; then
  echo "Aborting. Can not unpack installer."
  exit 1
fi

cd install-tl-20*
TLIVEV="`head -1 release-texlive.txt |cut -d" " -f5`"

if [ ! -d /opt/texlive/texmf-local ]; then
  echo "An administrative user needs to create the /opt/texlive/texmf-local directory and assign it texlive:texlive permissions."
  echo "To create that directory from an administrative account:"
  echo ""
  echo "sudo mkdir -p /opt/texlive/texmf-local"
  echo "sudo chown texlive:texlive /opt/texlive/texmf-local"
  exit 1
fi
USER="`ls -la /opt/texlive/texmf-local |grep " \.$"`"
if [[ "${USER}" != *"texlive texlive"* ]]; then
  echo "An administrative user needs to assign texlive:texlive ownership to the /opt/texlive/texmf-local directory."
  echo "To fix directory permissions from an administrative account:"
  echo ""
  echo "sudo chown -R texlive:texlive /opt/texlive/texmf-local"
  exit 1
fi

if [ ! -d "/opt/texlive/${TLIVEV}" ]; then
  echo "An administrative user needs to create the /opt/texlive/${TLIVEV} directory and assign it texlive:texlive permissions."
  echo "To create that directory from an administrative account:"
  echo ""
  echo "sudo mkdir /opt/texlive/${TLIVEV}"
  echo "sudo chown texlive:texlive /opt/texlive/${TLIVEV}"
  exit 1
fi
USER="`ls -la "/opt/texlive/${TLIVEV}" |grep "\.$"`"
if [[ "${USER}" != *"texlive texlive"* ]]; then
  echo "An administrative user needs to assign texlive:texlive ownership to the /opt/texlive/${TLIVEV} directory."
  echo "To fix directory permissions from an administrative account:"
  echo ""
  echo "sudo chown -R texlive:texlive /opt/texlive/${TLIVEV}"
  exit 1
fi

if [ -f "/opt/texlive/${TLIVEV}/texmf-dist/ls-R" ]; then
  echo "TeXLive ${TLIVEV} is already installed"
  exit 1
fi

# install it

/usr/bin/perl ./install-tl \
  --texdir="/opt/texlive/${TLIVEV}" \
  --texmflocal=/opt/texlive/texmf-local \
  --no-interaction



popd > /dev/null 2>&1



exit 0
