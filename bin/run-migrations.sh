#! /bin/bash

docker exec \
  -it \
  py-lyfe-app \
  ./bin/run-migrations.sh
