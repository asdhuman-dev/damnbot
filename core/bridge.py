from typing import Any
from aiogram.types import Message
from pygoridge import create_relay, RPC, SocketRelay  # type: ignore


class Bridge:
    def __init__(self, host: str = "127.0.0.1", port: int = 6001):
        self.host = host
        self.port = port
        self.socketrelay = None
        self.rpc = None
        self._connect()  # initial conn

    def _connect(self):
        print(f"Connecting to {self.host}:{self.port}")
        try:
            self.socketrelay = SocketRelay(self.host, self.port)
            self.socketrelay.connect()
            self.rpc = RPC(self.socketrelay)
        except Exception as e:
            print(f"Error connecting: {e}")
            self.socketrelay = None

    def send_rpc(self, method: str, payload: Any) -> Any:
        if self.socketrelay:
            try:
                return self.rpc(method, payload)
            except:
                self._connect()
                return self.rpc(method, payload)
        raise Exception("no socketrelay!")
