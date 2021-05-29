USERS = {}

def register(name, address):
    USERS[name] = address

def check_user(address):
    for user in USERS:
        if(USERS[user] == address):
            return user
    return 0
         
def get_address(name):
    if name in USERS:
        return USERS[name]

