"""
https://stackoverflow.com/questions/50678184/how-to-pass-additional-parameters-to-handle-client-coroutine
"""
import asyncio
import pickle
import base64
import sys
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN
import os

class TcpServer:
    def __init__(self, loop_asyncio):
        self._nc = NATS()
        self._sc = STAN()
        self._loop = loop_asyncio
        self._nats_endpoint = os.environ['NATS_ENDPOINT'] if "NATS_ENDPOINT" in os.environ else "192.168.0.101:4222"
        self._nats_cluster_name = os.environ['NATS_CLUSTER_NAME'] if "NATS_CLUSTER_NAME" in os.environ else "test-cluster"
        self._nats_client_id = os.environ['NATS_CLIENT_ID'] if "NATS_CLIENT_ID" in os.environ else "cl-1"
        
    async def handle_echo(self, reader, writer):
        await self._nc.connect(self._nats_endpoint, io_loop=self._loop) 
        await self._sc.connect(self._nats_cluster_name, self._nats_client_id, nats=self._nc)

        while True:
            try:
                data = await reader.readuntil(separator=b':')
                await self._sc.publish("raw.video", data[:-1])
            except:
                print("Unexpected error:", sys.exc_info()[0])
                break

        await self._sc.close()
        await self._nc.close()

loop = asyncio.get_event_loop()
tcp_server = TcpServer(loop)
coro = asyncio.start_server(tcp_server.handle_echo, '0.0.0.0', 8080, loop=loop)
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