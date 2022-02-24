#! /bin/sh

source .venv/bin/activate \
  && alembix -x db=dev revision --autogenerate -m 'autogen' \
  && alembic -x db=dev upgrade head
