FROM golang:1.12.1-alpine3.9

WORKDIR /go/src/app
RUN apk add --no-cache git
RUN go get github.com/nats-io/go-nats-streaming
RUN apk del git
COPY . .
RUN go build main.go
CMD [ "./main" ]