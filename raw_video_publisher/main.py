"""
https://stackoverflow.com/questions/50678184/how-to-pass-additional-parameters-to-handle-client-coroutine
"""
import asyncio
import pickle
import base64
import sys
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN

class TcpServer:
    def __init__(self, loop_asyncio):
        self._nc = NATS()
        self._sc = STAN()
        self._loop = loop_asyncio
        
    async def handle_echo(self, reader, writer):
        await self._nc.connect("192.168.0.101:4222", io_loop=self._loop)
        await self._sc.connect("test-cluster", "client-1", nats=self._nc)

        while True:
            try:
                data = await reader.readuntil(separator=b':,')
                await self._sc.publish("raw.video", data[:-2])
            except:
                print("Unexpected error:", sys.exc_info()[0])
                break

        await self._sc.close()
        await self._nc.close()

loop = asyncio.get_event_loop()
tcp_server = TcpServer(loop)
coro = asyncio.start_server(tcp_server.handle_echo, '127.0.0.1', 8080, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()