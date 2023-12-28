import json
from tidal_dl import TOKEN, getProfilePath, SETTINGS, getTokenPath, loginByWeb


def create_tidal_token():
    profile_path = getProfilePath()
    with open(profile_path, 'w', encoding='utf-8') as settings:
        settings.write(json.dumps({'apiKeyIndex': 4}))
    SETTINGS.read(profile_path)
    TOKEN.read(getTokenPath())
    loginByWeb()
    print(TOKEN.refreshToken)


if __name__ == '__main__':
    create_tidal_token()
