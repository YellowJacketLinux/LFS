#!/usr/bin/env bash

tlmgr update --self

if [ $? -eq 0 ]; then
  tlmgr update --all
fi
