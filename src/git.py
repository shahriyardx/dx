import getpass

import keyring


def save_token(token: str):
    keyring.set_password("dx", getpass.getuser(), token)


def get_token():
    token = keyring.get_password("dx", getpass.getuser())
    return token

def get_or_save_token(token):
    if token:
        save_token(token)

    token = get_token()
    return token