#!/usr/bin/env bash
FILES=$(git ls-files --cached --modified --others \
  --exclude 'venv' \
   "$(git rev-parse --show-toplevel)/*.py" | grep -v /migrations/ | grep -v 'test.*.py' | sort | uniq)
CHECK_OPTIONS="--pretty --show-error-codes"
dmypy run -- $CHECK_OPTIONS $FILES
