#!/bin/python

import time
import uuid

def postTweet(uid, msg) :
	"post a tweet"
	t = str(uuid.uuid4())
	timestamp = long(time.time() * 1e6)
	value = {'body':msg, 'user':uid, 'timestamp':timestamp}
	insert('TWEETS', t, value)

	insert('USERLINE', uid, {timestamp:t})

	for followerID in get('FOLLOWER', uid):
    		insert('TIMELINE', followerID, {timestamp:t})



def postReply(tid, uid, msg) : 
	"reply to a tweet"
	t = str(uuid.uuid4())
	timestamp = long(time.time() * 1e6)
	value = {'body':msg, 'user':uid, 'timestamp':timestamp}

	insert('TWEETS', t, value)
	insert('TWEETS', tid, {timestamp:t})


def parseTweet(msg) :

#	generate list for trends and tagged people
# 	return the 2 lists 

# add code for finding '@' and '#'
