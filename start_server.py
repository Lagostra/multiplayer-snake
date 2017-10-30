from server.main import Server
from common import preferences

preferences.load()
preferences.save()

server = Server(47777)
server.start()