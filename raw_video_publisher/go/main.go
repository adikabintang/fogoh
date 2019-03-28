package main

import (
	"./tcp_server"
	stan "github.com/nats-io/go-nats-streaming"
)

func main() {
	server := tcp_server.New("0.0.0.0:8080")
	sc, _ := stan.Connect("test-cluster", "clientID")

	server.OnNewMessage(func(c *tcp_server.Client, message string) {
		sc.Publish("foo", []byte(message[:len(message)-1]))
	})

	server.Listen()
}
