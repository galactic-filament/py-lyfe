#! /bin/bash

docker run \
  -it \
  -p 5432:5432 \
  --rm \
  --network py-lyfe \
  -e POSTGRES_PASSWORD=password \
  --name py-lyfe-postgres \
  postgres
