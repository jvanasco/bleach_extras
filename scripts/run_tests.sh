#!/bin/bash

# originally in bleach https://github.com/mozilla/bleach
# bleach is covered by the Apache License, Version 2.0

# Make sure we're running from the bleach repository directory and
# not this directory.
THISDIR=$(basename `pwd`)
if [[ "${THISDIR}" == "scripts" ]]; then
    cd ..
fi

MODE=${1:-test}

case "${MODE}" in
  test)
    pytest ;;
  lint)
    flake8 bleach_extras/ ;;
  *)
    echo "Unknown mode $MODE."
    exit 1
esac
