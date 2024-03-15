#!/bin/bash

# 需要 benchmark-src 先 build

if [ -d "./dist" ]; then
  rm -r dist
fi
cp -r ../benchmark-src/dist ./dist

docker rm -f vkn-benchmark-api

docker run --name vkn-benchmark-api \
    --restart=always \
    -v `pwd`/dist/:/usr/share/nginx/html \
    -p 8000:80 \
    -d nginx:alpine