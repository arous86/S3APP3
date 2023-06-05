#!/bin/sh

mkdir -p $(pwd)/tmp_todo
docker run -it --rm --name app3s3i-arret01 --mount type=bind,source="$(pwd)"/tmp_todo,target=/todo arret01 sh
