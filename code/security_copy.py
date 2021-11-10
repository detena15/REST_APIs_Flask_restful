users = [
    {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
]

# Asociar la informacion del usuario a varias keys: username (bob) y userid (1)
username_mapping = {
    'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}

userid_mapping = {
    1: {
        'id': 1,
        'username': 'bob',
        'password': 'asdf'
    }
}


def authenticate(username, password):
    # Find an user by the username
    user = username_mapping.get(username, None)

    if user and user.password == password:
        return user


def identity(payload):  # The payload is the contects of the JWT (json web token)
    # Extract the user_id from that payload
    user_id = payload['identity']

    return userid_mapping.get(user_id, None)
