import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("progress_bar", self.channel_name)
        await self.accept()


    async def receive(self, text_data):
        print("RECEIVED :", text_data)
        data = json.loads(text_data)
        message = data['message']

        await self.send(text_data=json.dumps({
            'progress': 0
        }))
        
    
    async def send_progress(self, event):
        progress_value = event['progress']
        await self.send(text_data=json.dumps({
            'progress': progress_value
        }))


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("progress_bar", self.channel_name)
