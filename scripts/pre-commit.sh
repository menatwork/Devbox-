#!/bin/sh
set -eu

cd "$(git rev-parse --show-toplevel)"

{
  cd devbox-py

  printf "\npre-commit: devbox-py: pipenv run check-types\n"
  pipenv run check-types

  #printf "\npre-commit: devbox-py: pipenv run check-style\n"
  #pipenv run check-style
}

printf "\npre-commit: all good\n"