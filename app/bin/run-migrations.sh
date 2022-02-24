#! /bin/sh

source .venv/bin/activate \
  && alembic -x db=dev upgrade head \
  && alembic -x db=dev revision --autogenerate -m 'autogen' \
  && alembic -x db=dev upgrade head
