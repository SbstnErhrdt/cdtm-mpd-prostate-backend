import requests


def get_photos():
    # secret: 6d1af18d28a9452990a16d9b59362a2b
    # Client ID: 4b5a77e548f94ba9ad5b2ca0f2e3a073
    r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    return r.json()
