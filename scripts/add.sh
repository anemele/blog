#!/usr/bin/bash

if [ -z "$1" ]; then
  echo "require post FILE name, such as a-b-c.md"
  exit
fi

hugo new content post/$(date +%Y/%m)/"$1"
