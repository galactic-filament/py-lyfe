#! /bin/sh

source .venv/bin/activate \
  && alembic -x db=dev upgrade head
