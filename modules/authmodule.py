from config.settings import user_dict,roles

def isvalid(username,password): 
    dictU=user_dict[username]
    dictP = user_dict[username]['password']
    print(f"{username==dictU} {password==dictP} {user_dict[username]} {user_dict[username]['password']}")
    if (username in user_dict and password == dictP):
        return True
    else:
        return False

class Auth():
    def __init__(self) -> None:
        pass
    