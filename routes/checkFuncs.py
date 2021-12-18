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


'''by mahbod ghadiri sani'''
'''
This one checks if password ONLY contains letters, digits and _ 
password must be between 6 to 32 characters 
'''
def checkPassword(password):
    regex='^[a-zA-Z0-9_]{6,32}$'

    if re.match(regex,password):
        return True
    else :
        return False



'''
This one is not what you asked for, but i believe is the the more practical of the two.
It only accept letters, numerals and _
each password must contain at least ONE upercase and ONE lowercase letter
additionally passwords must contain at least ONE digit and _
length of the password must be between 6 to 32

'''
def checkStrongPassword(password):
    regex = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)+(?=.*[_])[a-zA-Z0-9_]{6,32}$'
    if re.match(regex,password) : 
        return True
    else :
        return False