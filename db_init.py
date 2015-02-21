import sqlite3

main_con = sqlite3.connect("db/main.db")
main_con.isolation_level = None
m = main_con.cursor()

m.execute("CREATE TABLE IF NOT EXISTS Users (id int, name text, mail text, hash text, salt text, lkarma int, ckarma text)")
m.execute("CREATE TABLE IF NOT EXISTS Posts (id int, poster int, title text, self boolean, body text, vtable text)")

main_con.close()


votes_con = sqlite3.connect("db/votes.db")
votes_con.isolation_level = None
v = votes_con.cursor()

#v.execute("CREATE TABLE Users (id int, name text, mail text, hash text, salt text, lkarma int, ckarma text)")

votes_con.close()