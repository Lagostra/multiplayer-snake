from client.main import Client
from common import preferences

preferences.load()
preferences.save()

client = Client(preferences.preferences['resolution'])
client.start()
