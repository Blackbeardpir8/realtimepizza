from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class YourConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "main_room"
        self.group_name = self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.accept()
        
        # Send confirmation message
        self.send(text_data=json.dumps({
            "message": "Connected to WebSocket"
        }))
        print("WebSocket connection established and message sent.")

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Echo the message back to WebSocket
        self.send(text_data=json.dumps({
            "message": message
        }))
        print(f"Message received: {message}")

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
