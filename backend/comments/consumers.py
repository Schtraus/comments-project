import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("comments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def send_new_comment(self, event):
        # await asyncio.sleep(0.3)
        await self.send(text_data=json.dumps(event["data"]))
