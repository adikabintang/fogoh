IMAGE_NAME=streamer-to-nginx
PREFIX=adikabintang/streamer-to-nginx
TAG=latest

.PHONY: docker
docker:
	docker build -t $(IMAGE_NAME) .

.PHONY: push
push:
	docker tag $(IMAGE_NAME) $(PREFIX):$(TAG)
	docker push $(PREFIX):$(TAG)
