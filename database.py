USERS = {}

def register(name, address):
    USERS[name] = address

def get_user(address):
    for user in USERS:
        if(USERS[user] == address):
            return user
    return 0
         
def get_address(name):
    if name in USERS:
        return USERS[name]

def logout(address):
    user = get_user(address)
    if(user != 0):
        USERS.pop(user)
