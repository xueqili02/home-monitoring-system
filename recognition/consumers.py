import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ObjectDetectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video_name = self.scope["url_route"]["kwargs"]["video_name"]
        self.video_group_name = f"video_{self.video_name}"

        # Join video group
        await self.channel_layer.group_add(self.video_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave video group
        await self.channel_layer.group_discard(self.video_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(
            self.video_group_name, {"type": "object.detect", "message": text_data}
        )


    async def object_detect(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({"message": message}))