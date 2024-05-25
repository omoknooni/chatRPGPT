import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime

class GameConsumer(AsyncWebsocketConsumer):
    # Connect to WebSocket
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f'game_{self.session_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    # Disconnect from WebSocket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket, 사용자가 웹소켓으로 발송한 메시지의 처리
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        timestamp = str(datetime.now())

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'timestamp': timestamp
            }
        )

    # Send message to WebSocket, 사용자가 웹소켓으로 발송한 메시지를 동일 그룹 사용자들에게 전송
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
