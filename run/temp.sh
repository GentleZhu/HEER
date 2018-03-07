#!/bin/bash

# find root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
#script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
script_dir="$( dirname "$SOURCE" )"
root_dir="$( dirname $script_dir )"

echo $root_dir
