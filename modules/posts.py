# Local imports
from connect import m,v
from crypto import *

#NOTE: SQL '?' tuples must use '_t' as var name
#NOTE: the tuples that fetch(one|all)() returns should be called 'res'

#######################
#     POST CLASS      #
#######################
# IDs and names are stored as fields because they
# are used to query the database. Everything else
# is queried itself.

class Post:
    def __init__(self, id):
        self.id = id
        _t = (self.id,)
        m.execute("SELECT vtable FROM Posts WHERE id = ?", _t)
        res = m.fetchone()
        self.vtable = res[0]
    
    def vote(self, user, vote=True):
        _t = (user,)
        # Check for already-voted
        v.execute("SELECT 1 FROM "+self.vtable+" WHERE user = ?", _t)
        if v.fetchone():
            # Un-vote
            v.execute("DELETE FROM "+self.vtable+" WHERE user = ?", _t)
            return False
        else:
            # Vote
            _t = (user, int(vote))
            v.execute("INSERT INTO "+self.vtable+" (user, vote) VALUES(?, ?)", _t)
            return True
        
    def get_score(self):
        v.execute("SELECT (SELECT COUNT(vote) FROM "+self.vtable+" WHERE vote = 1) - (SELECT COUNT(vote) FROM "+self.vtable+" WHERE vote = 0)")
        res = v.fetchone()
        return res[0]
    
    def get_upvoters(self):
        v.execute("SELECT user FROM "+self.vtable+" WHERE vote = 1")
        res = v.fetchall()
        return [t[0] for t in res] # Remove tuples
    def get_downvoters(self):
        v.execute("SELECT user FROM "+self.vtable+" WHERE vote = 0")
        res = v.fetchall()
        return [t[0] for t in res] # Remove tuples
        

#######################
#    POST ACTIONS     #
#######################  TODO ADD USER AND POST ALLOWEDCHAR ETC.

def new_post(posterid, title, body, self=False):
    id = get_new_id()
    if not self:
        self = 0
    else:
        self = 1
    vtable = get_new_vtable()
    _t = (id, posterid, title, self, body, vtable)
    m.execute("INSERT INTO Posts (id, poster, title, self, body, vtable) VALUES(?,?,?,?,?,?)", _t)
    return True


######################
#    POST GETTERS    #
######################

def get_post(id):
    return Post(id)




#######################
#        MISC         #
#######################


def get_new_id():
    m.execute("SELECT id FROM Posts WHERE id = ( SELECT MAX(id) FROM Posts )")
    res = m.fetchone()
    if not res: # No posts
        return 0
    else:
        return int(res[0])+1

def get_new_vtable():
    table = get_rstring()
    v.execute("CREATE TABLE "+table+" (user int, vote int)")
    return table
