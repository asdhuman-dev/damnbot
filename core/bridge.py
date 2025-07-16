from aiogram.types import Message
from pygoridge import create_relay, RPC, SocketRelay

rpc = RPC(SocketRelay("127.0.0.1", 6001))
unix_relay = create_relay("unix:///tmp/rpc.sock")

print(rpc("App.Test", "string from python"))


def send_update(data: str):
    rpc("App.ProcessUpdates", data)
