import json
import logging
import asyncio
import websockets

from datasource.okex.dispatcher import Dispatcher
from datasource.okex.parser import ParserFactory


class CollectionError(Exception):
    """"""


class OkexWsDatasource:
    __uri__ = "wss://wsaws.okex.com:8443/ws/v5/public"  # noqa
    __ping_interval__ = 20

    def __init__(self, parser_factory: "ParserFactory", msg_dispatcher: "Dispatcher"):
        self.received_pong = False
        self.parser_factory: "ParserFactory" = parser_factory
        self.msg_dispatcher = msg_dispatcher

    async def ping(self, ws):
        await asyncio.sleep(self.__ping_interval__)
        logging.info('发送ping')
        await ws.send("ping")
        self.received_pong = False
        await asyncio.sleep(self.__ping_interval__)
        if not self.received_pong:
            raise CollectionError('未收到pong')

    async def subscribe(self, topic: str):
        while True:
            try:
                await self._do_subscribe(topic)
            except Exception as e:
                logging.exception(e)
                logging.info('即将重新连接')

    async def _do_subscribe(self, topic: str):
        async with websockets.connect(self.__uri__) as ws:
            await ws.send(topic)
            msg = await ws.recv()
            msg = json.loads(msg)
            assert msg['event'] == 'subscribe', msg
            ping = asyncio.create_task(self.ping(ws))
            while True:
                try:
                    msg = await ws.recv()
                    if msg == 'pong':
                        logging.info('收到pong')
                        self.received_pong = True
                    else:
                        msg = json.loads(msg)
                        channel = msg['arg']['channel']
                        queue = self.msg_dispatcher.get_queue(channel)
                        msg = self.parser_factory.get_parser(channel).parse(msg)
                        await queue.put(msg)
                    ping.cancel()
                    ping = asyncio.create_task(self.ping(ws))
                except Exception as e:
                    logging.exception(e)
                    break
