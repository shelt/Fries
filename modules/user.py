# Local imports
from connect import m
from crypto import *

#NOTE: SQL '?' tuples must use '_t' as var name
#NOTE: the tuples that fetch(one|all)() returns should be called 'res'

#######################
#     USER CLASS      #
#######################
# IDs and names are stored as fields because they
# are used to query the database. Everything else
# is queried itself.

class User:
    def __init__(self, id):
        self.id = id
        
    def get_name(self):
        _t = (self.id,)
        m.execute("SELECT name FROM Users WHERE id = ?", _t)
        res = m.fetchone()
        return res[0]
    
    def mod_lkarma(self, inc=True):
        if inc:
            delta = "+1"
        else:
            delta = "-1"
        _t = (self.id,self.id)
        m.execute("UPDATE Users SET lkarma = ( ( SELECT lkarma FROM Users WHERE id = ? ) "+delta+" ) WHERE id = ?", _t)
    def mod_ckarma(self, inc=True):
        if inc:
            delta = "+1"
        else:
            delta = "-1"
        _t = (self.id,self.id)
        m.execute("UPDATE Users SET ckarma = ( ( SELECT ckarma FROM Users WHERE id = ? ) "+delta+" ) WHERE id = ?", _t)
        
    def get_lkarma(self):
        _t = (self.id,)
        m.execute("SELECT lkarma FROM Users WHERE id = ?", _t)
        res = m.fetchone()
        return res[0]
    def get_ckarma(self):
        _t = (self.id,)
        m.execute("SELECT ckarma FROM Users WHERE id = ?", _t)
        res = m.fetchone()
        return res[0]
        

#######################
# USERACCOUNT ACTIONS #
#######################
# Functions related to user auth and
# other account-related activities.

def new_user(username, password, email):
    if username_exists(username):
        return False
    id = get_new_id()
    salt = get_salt()
    hash = get_hash(password, salt)
    _t = (id, username, email, hash, salt, 0, 0)
    m.execute("INSERT INTO Users (id, name, mail, hash, salt, lkarma, ckarma) VALUES(?,?,?,?,?,?,?)", _t)
    return True

def verify_user(username, password):
    _t = (username,)
    m.execute("SELECT * FROM Users WHERE name IS ?", _t)
    res = m.fetchone()
    assert res[1] == username
    if get_hash(password, res[4]) == res[3]:
        return True
    else:
        return False

def username_exists(username):
    _t = (username,)
    m.execute("SELECT COUNT(1) FROM Users WHERE name IS ?", _t)
    if m.fetchone()[0] == 1:
        return True


######################
#    USER GETTERS    #
######################
# These functions get Users.
# Getting user-specific data is done objectively.

# BULK GETTERS

def get_users():
    users = []
    m.execute("SELECT id FROM Users")
    for res in m.fetchall():
        user = User(res[0])
        users.append(user)
    return users
    
def get_users_by_mail(mail):
    users = []
    _t = (mail,)
    m.execute("SELECT id FROM Users WHERE mail IS ?", _t)
    for res in m.fetchall():
        user = User(res[0])
        users.append(user)
    return users

# SINGLE GETTERS

def get_user(id):
    return User(id)

def get_user_by_name(name):
    _t = (name,)
    m.execute("SELECT id FROM Users WHERE name IS ?", _t)
    res = m.fetchone()
    return User(res[0])


#######################
#        MISC         #
#######################

def get_new_id():
    m.execute("SELECT id FROM Users WHERE id = ( SELECT MAX(id) FROM Users )")
    res = m.fetchone()
    if not res: # No users
        return 0
    else:
        return int(res[0])+1

