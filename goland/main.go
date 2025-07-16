package main

import (
	"fmt"
	"net"
	"net/rpc"

	"github.com/spiral/goridge"
)

type App struct{}

func (s *App) Test(name string, r *string) error {
	*r = fmt.Sprintf("Hello from go, %s!", name)
	return nil
}

func (s *App) ProcessUpdates(object any, r *bool) error {
	// bool will control if python side should process the message

	fmt.Println(object)
	// *r = fmt.Sprintf("Got this piece of shit: %s", object)
	*r = true
	return nil
}

func main() {
	ln, err := net.Listen("tcp", ":6001")
	if err != nil {
		panic(err)
	}

	rpc.Register(new(App))

	for {
		conn, err := ln.Accept()
		if err != nil {
			continue
		}
		go rpc.ServeCodec(goridge.NewCodec(conn))
	}
}
