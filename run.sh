#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 FILENAME.forth [arguments ...]"
  exit 1
fi

filename="$1"
shift

python3 MainRunner.py "$filename" "$@"