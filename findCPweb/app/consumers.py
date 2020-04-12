import json
import logging
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
	def connect(self):
		print("connect")
		#self.send(message.reply_channel, {"accept": True})
		self.accept()

	def receive(self, text_data):
		channel_layer = get_channel_layer()
		print("received: ", text_data)		
		try:
			data = json.loads(text_data)
			print(data)
		except ValueError:
			print("el formato no parece json=%s", text_data)
			return
		if data:
			reply_channel = self.channel_name
			print( str(json.dumps({"channel":reply_channel})) )
			self.send( str(json.dumps({"channel":reply_channel})) )
		return False

	def ws_send(self, event):
		front_response = event.get('text', None)
		if front_response is not None:
			compiled_response_data = json.loads(front_response)

		# Send message to WebSocket
		self.send(json.dumps(compiled_response_data))

	def disconnect(self, close_code):
		#Group("group_name").discard(message.reply_channel)
		pass
