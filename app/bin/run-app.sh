#! /bin/sh

source .venv/bin/activate \
  && python ./py_lyfe/validate-environment.py \
  && python -m py_lyfe
