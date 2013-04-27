import hashlib
import web
import sqlite3

def checkpw(username, password):
    authdb = sqlite3.connect('users.db')
    cur = authdb.cursor()
    pwdhash = hashlib.sha512(password).hexdigest()
    cur.execute('select * from users where username=? and password=?', (username, pwdhash))
    if cur.fetchone(): 
    	return True
    else:
    	return False

def authuser(username, password):
    if checkpw(username, password):
        web.setcookie("session", username)
