#!/bin/python

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

def addTweet(n) :
	"add tweet into db"

	n=input("Enter number")



pool = ConnectionPool('Keyspace1')
tweets = ColumnFamily(pool, 'tweets')
#insert into tweets (tweet) values ('twwet from code')
abc = {'tweet': 'this is my tweet through code.'}
tweets.insert('5',abc)
#a = "column_reversed=True"
print tweets.get('1')
#addTweet();
print "tweet added"