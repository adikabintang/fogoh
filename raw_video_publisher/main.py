"""
inspiration: 
https://www.snip2code.com/Snippet/1347060/Example-of-asyncio-nats-and-threads-usin
"""
import asyncio
import time
import socket, struct
from threading import Thread
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
import cv2, pickle

class Component(object):
    def __init__(self, nc, loop):
        self.nc = nc
        self.loop = loop
        
    def run(self):
        yield from self.nc.connect(io_loop=self.loop)
        yield from self.nc.flush()

def another_thread(c):
    if not c.nc.is_connected:
        print("Not connected to NATS!")
        return

    HOST = "0.0.0.0"  
    PORT = 8080 
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(2)
    conn, addr = sock.accept()
    data = b""
    payload_size = struct.calcsize(">L")

    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
            if len(data) == 0:
                break
        
        if len(data) != 0:
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            asyncio.run_coroutine_threadsafe(
                c.nc.publish("raw.camera", 
                frame.tobytes()),
                loop=c.loop)
            
        else:
            conn, addr = sock.accept()
    

def main():
    nc = NATS()
    loop = asyncio.get_event_loop()
    component = Component(nc, loop)

    loop.run_until_complete(component.run())

    thr = Thread(target=another_thread, args=(component,))
    thr.start()

    loop.run_forever()

if __name__ == '__main__':
    main()