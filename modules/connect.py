# connect.py
# This file creates the global cursor objects
# 'close's are used to close the connection
# in the main files.

import sqlite3

main_con = sqlite3.connect("../db/main.db")
m = main_con.cursor()
main_con.isolation_level = None

votes_con = sqlite3.connect("../db/votes.db")
v = votes_con.cursor()
votes_con.isolation_level = None


main_close  = main_con.close
votes_close = votes_con.close