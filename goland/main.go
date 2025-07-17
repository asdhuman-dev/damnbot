package main

import (
	"encoding/json"
	"fmt"
	"log/slog"
	"net"
	"net/rpc"

	"github.com/asdhuman-dev/damnbot/types/general"
	"github.com/spiral/goridge"
)

type App struct{}

func (s *App) Test(name string, r *string) error {
	*r = fmt.Sprintf("Hello from go, %s!", name)
	return nil
}

// bool will control if python side should process the message
func (s *App) ProcessUpdates(update string, r *bool) error {
	v := general.Update{}

	json.Unmarshal([]byte(update), &v)

	slog.Info(
		fmt.Sprintf("Got message '%s' from %s", v.Message.Text, v.Message.From.FirstName),
	)

	*r = true
	return nil
}

func main() {
	slog.SetLogLoggerLevel(slog.LevelDebug)

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
