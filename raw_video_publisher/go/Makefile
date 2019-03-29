IMAGE_NAME=fogoh-raw-vid-pub-go
PREFIX=adikabintang/fogoh-raw-vid-pub-go
TAG=latest

.PHONY: docker
docker:
	docker build -t $(IMAGE_NAME) .

.PHONY: push
push:
	docker tag $(IMAGE_NAME) $(PREFIX):$(TAG)
	docker push $(PREFIX):$(TAG)
