from server.main import Server
from common import preferences

preferences.load()
preferences.save()

server = Server(preferences.preferences['port'])
server.start()