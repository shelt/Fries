# Local imports
from connect import main_close,votes_close
from user import *
from posts import *



# Various testing...

new_user('test0', 'test', 'test@mail.com')
new_user('test1', 'test', 'test@mail.com')
new_user('test2', 'test', 'test@mail.com')
new_user('test3', 'test', 'test@mail.com')
new_user('test4', 'test', 'test@mail.com')
new_user('test5', 'test', 'test@mail.com')


new_post(0, "Check out this funny website", "http://www.theonion.com/")
p = get_post(0)

p.vote(0, False) #Dvote
p.vote(1, True)  #Uvote
p.vote(2, False)
p.vote(3, False)
p.vote(4, True)
p.vote(5, True)

for id in p.get_downvoters():
    print get_user(id).get_name()

main_close()
votes_close()