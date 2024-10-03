# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'  # Define your group name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Process the message and create a response
        response_message = self.process_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response_message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    def process_message(self, message):
        message = message.lower()  # Normalize the message to lowercase

        # Basic keyword responses
        if 'hello' in message or 'hi' in message:
            return "Hello! How can I assist you today?"
        elif 'bye' in message or 'goodbye' in message:
            return "Goodbye! Have a great day!"
        elif 'how are you' in message:
            return "I'm just a bot, but I'm here to help you!"
        elif 'help' in message:
            return "Sure! What do you need help with?"
        elif 'weather' in message:
            return "I can't check the weather, but you can try looking it up online!"
        elif 'your name' in message:
            return "I am a chat bot created for assistance. You can call me ChatBot!"
        elif 'what can you do' in message:
            return "I can chat with you and help answer simple questions!"
        elif 'joke' in message:
            return "Why did the scarecrow win an award? Because he was outstanding in his field!"
        elif 'quote' in message:
            return "The only limit to our realization of tomorrow is our doubts of today."
        elif 'date' in message:
            from datetime import datetime
            return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
        else:
            return "I'm not sure how to respond to that. Can you ask something else?"