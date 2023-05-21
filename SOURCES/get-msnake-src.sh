#!/bin/bash

echo "Warning: check https://github.com/mogria/msnake for latest commit"

sleep 5

MYTEMP=`mktemp -d msnake.XXXXXXXXXXXX`
pushd ${MYTEMP}

git clone git@github.com:mogria/msnake.git
mv msnake msnake-20200201

tar -jcf msnake-20200201.tar.bz2 msnake-20200201
popd
mv ${MYTEMP}/msnake-20200201.tar.bz2 .
rm -rf ${MYTEMP}

# EOF
