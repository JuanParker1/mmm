import json
import logging
import asyncio
import websockets

from .parser import ParserFactory, parser_factory
from events import default_dispatcher, Event


class CollectionError(Exception):
    """"""


class OkexWsDatasource:
    __uri__ = "wss://wsaws.okex.com:8443/ws/v5/public"  # noqa
    __ping_interval__ = 20

    def __init__(self, factory: "ParserFactory" = parser_factory):
        self.received_pong = False
        self.parser_factory: "ParserFactory" = factory

    async def ping(self, ws):
        await asyncio.sleep(self.__ping_interval__)
        logging.info('发送ping')
        await ws.send("ping")
        self.received_pong = False
        await asyncio.sleep(self.__ping_interval__)
        if not self.received_pong:
            raise CollectionError('未收到pong')

    def subscribe(self, topic: str):
        async def create_task():
            while True:
                try:
                    await self._do_subscribe(topic)
                except Exception as e:
                    logging.exception(e)
                    logging.info('即将重新连接')
        loop = asyncio.get_event_loop()
        loop.create_task(create_task(), name=f'okex-ws-sub-{topic}')

    async def _do_subscribe(self, topic: str):
        async with websockets.connect(self.__uri__, ping_interval=None) as ws:
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
                        event = self.parser_factory.get_parser(channel).parse(msg)
                        if isinstance(event, Event):
                            await default_dispatcher.dispatch(event)
                        elif isinstance(event, list):
                            for each in event:
                                await default_dispatcher.dispatch(each)
                    ping.cancel()
                    ping = asyncio.create_task(self.ping(ws))
                except Exception as e:
                    logging.exception(e)
                    break
