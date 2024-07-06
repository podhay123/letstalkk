from cmath import log
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from django.contrib.auth.decorators import login_required
from openai import OpenAI


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            print(self.user)
        else:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        user = str(self.user)
        print(user)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if text_data_json["generate_topic"] == True:
            openai = OpenAI(
                # enter your key below
                api_key="",
                base_url="https://api.deepinfra.com/v1/openai",
            )

            chat_completion = openai.chat.completions.create(
                model="openchat/openchat-3.6-8b",
                messages=[
                    {
                        "role": "user",
                        "content": "Generate a great topic to talk about. Try to use answers which are not ai like topics. Use only one word. Your anwser should be short, simple and be like like 'trees' or 'flowers'.",
                    }
                ],
            )

            message = chat_completion.choices[0].message.content
            message = "Let's talk about:" + message
            user = "AI"
        message = "[" + user + "] " + message
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message},
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
