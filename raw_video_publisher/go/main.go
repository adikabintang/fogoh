package main

import (
	"os"

	"./tcp_server"
	stan "github.com/nats-io/go-nats-streaming"
)

func main() {
	nats_endpoint := os.Getenv("NATS_ENDPOINT")
	if len(nats_endpoint) == 0 {
		nats_endpoint = "192.168.0.101:4222"
	}

	nats_cluster_name := os.Getenv("NATS_CLUSTER_NAME")
	if len(nats_cluster_name) == 0 {
		nats_cluster_name = "test-cluster"
	}

	nats_client_id := os.Getenv("NATS_CLIENT_ID")
	if len(nats_client_id) == 0 {
		nats_client_id = "cl-1"
	}

	url_option := stan.NatsURL(nats_endpoint)
	server := tcp_server.New("0.0.0.0:3000")
	sc, _ := stan.Connect(nats_cluster_name, nats_client_id, url_option)

	server.OnNewMessage(func(c *tcp_server.Client, message string) {
		sc.Publish("raw.video", []byte(message[:len(message)-1]))
	})

	server.Listen()
}
