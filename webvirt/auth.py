import hashlib

def checkpw(username, password):
    authdb = sqlite3.connect('users.db')
    pwdhash = hashlib.sha512(password).hexdigest()
    check = authdb.execute('select * from users where username=? and password=?', (username, pwdhash))
    if check: 
    	return True
    else:
    	return False
