import json

PREFERENCES_FILE = 'preferences.json'

preferences = {
    'resolution': (800, 600),
    'fullscreen': False,
    'server': 'localhost',
    'port': 47777,
    'username': 'Anonymous',
}

def load():
    try:
        with open(PREFERENCES_FILE, 'r') as file:
            prefs = json.loads(file.read())

            for key, value in prefs.items():
                preferences[key] = value

            preferences['resolution'] = tuple(preferences['resolution'])
    except FileNotFoundError:
        return

def save():
    with open(PREFERENCES_FILE, 'w') as file:
        file.write(json.dumps(preferences, indent=4, sort_keys=True))