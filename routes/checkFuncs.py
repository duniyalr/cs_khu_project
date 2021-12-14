import re
'''
    this function checks email address format
    by yousef osanlo
'''
def checkEmail(email):
    email = email.lower()

    # import re   //// i add this line outside the function, so other funcs can use it too.

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

    if(re.search(regex, email)):   
        return True  
    else:   
        return False