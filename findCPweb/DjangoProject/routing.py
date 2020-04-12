#from channels import include

#channel_routing = [
#	include("app.routing.websocket_routing",path=r'^/ws'),
#]

from channels.auth import AuthMiddlewareStack
from django.conf.urls import url
from django.urls import path
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing

application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			app.routing.websocket_urlpatterns
		)
	),
})
