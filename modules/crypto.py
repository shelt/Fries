import hashlib
import uuid
from string import ascii_uppercase
from random import choice

def get_salt():
    return uuid.uuid4().hex

def get_hash(password, salt):
    return hashlib.sha512(password + salt).hexdigest()

def get_rstring():
    str = ""
    for i in range(10):
        str += choice(ascii_uppercase)
    return str