# create database blog.db

import sqlite3

with sqlite3.connect("blog.db") as connection:
    c = connection.cursor()
    c.execute('CREATE TABLE posts (name TEXT, post TEXT, date TEXT, time TEXT)')
    post_data = [("Zev", "OK, tomorrow let\'s pair up and try to build a Flask Blog.", "04-13-14", "05:20 pm"),
		("Brandon", "Yeah, that sounds like a good plan.", "04-13-15", "11:17 pm"),
		("Tom", "How about we set a time limit?", "04-14-15", "10:23 am"),
		("Mark", "We should work on it for 1 hour and then reconvene.", "04-14-15", "3:13 pm")]
    c.executemany('INSERT INTO posts VALUES(?, ?, ?, ?)', post_data)
	 
