#/bin/bash

docker build -t fogoh-raw-vid-pub-go .
TAG=$(docker images | grep -w "^fogoh-raw-vid-pub-go" | awk '{print $3}')
docker tag $TAG adikabintang/fogoh-raw-vid-pub-go:latest
docker push adikabintang/fogoh-raw-vid-pub-go:latest

