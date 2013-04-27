import hashlib
import web

def checkpw(username, password):
    authdb = sqlite3.connect('users.db')
    pwdhash = hashlib.sha512(password).hexdigest()
    check = authdb.execute('select * from users where username=? and password=?', (username, pwdhash))
    if check: 
    	return True
    else:
    	return False

def authuser(username, password):
    if checkpw(username, password):
        web.setcookie("session", username)
