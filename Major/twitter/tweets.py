#!/usr/bin/python
#!/flask/bin/python
from flask import Flask, request, jsonify

import time
import uuid
import operations as op

app = Flask(__name__)

def check_for_hashtag(body,timestamp,t):
	body = body.split("#");
	body = body[1:]
	for text in body:
		text = text.split(" ")
		text = text[0]
		value = {timestamp:t}
		op.insert('HASH_TAGS', text , value)

def check_for_reference(body,t,timestamp):
	body = body.split("@");
	body = body[1:]
	for text in body:
		text = text.split(" ")
		text = text[0]
		value = op.get('USERNAME',text)
		op.insert('USERLINE',value['uid'],{timestamp:t})

def parse(tid,uid):
	val = op.get('TWEETS',tid)
	timestamp = str(val['timestamp']) + ":" + str(val['user'])
	check_for_hashtag(val['body'],tid,timestamp)
	check_for_reference(val['body'],tid,timestamp)

def post_tweet(msg,uid):
        "post a tweet"
        t = str(uuid.uuid4())
        timestamp = long(time.time() * 1e6)
        value = {'body':msg, 'user':uid, 'timestamp':str(timestamp)}
        op.insert('TWEETS', t, value)
	timestamp = str(timestamp) + ":" + str(uid)
        op.insert('USERLINE', uid, {timestamp:t})
        op.insert('TIMELINE', uid, {timestamp:t})
#	parse(tid,uid)
	for followerID in op.get('FOLLOWER', uid):
		if 'status' != followerID:
               	   op.insert('TIMELINE', followerID, {timestamp:t})		#DO
	
	return jsonify({'tid':t,'body':msg,'user':uid})

def mark_as_favorite(uid,tid):
	val = is_favourite(uid,tid)
	if val:
		d = op.get('FAVORITE_IS', tid)
		t = d[uid]
		print "deleting favourite tweet with ", uid, t
		op.remove_column('FAVORITE_OF', uid,[t])
		op.remove_column('FAVORITE_IS', tid,[uid])		
	else:
		val = op.get('TWEETS',tid)
		print "TWEET to be marked as favourite", val
		timestamp = long(time.time() * 1e6)
		timestamp = str(timestamp)
		op.insert('FAVORITE_OF', uid,{timestamp:tid})
		op.insert('FAVORITE_IS', tid, {uid:timestamp})
	

def postReply(tid, uid, msg) :
        "reply to a tweet"
        t = str(uuid.uuid4())
        timestamp = long(time.time() * 1e6)
        value = {'body':msg, 'user':uid, 'timestamp':timestamp}
        op.insert('TWEETS', t, value)
        op.insert('REPLY_TO_TWEET', tid, {timestamp:t})
	for followerID in op.get('FOLLOWER', uid):
		op.insert('TIMELINE', followerID, {timestamp:t})		#DO

	#for favorite tweets

def delete_tweet(tweetid,uid) :
	"to delete a tweet"
	val = op.get('TWEETS',tweetid)
	op.remove_row('TWEETS', tweetid)
	key = str(val['timestamp']) + ":" + uid
	op.remove_column('USERLINE', uid, [key])				#delete from timeline and userline
	op.remove_column('TIMELINE', uid, [key])
	for followerID in op.get('FOLLOWER', uid):
		if 'status' != followerID:
			op.remove_column('TIMELINE', followerID, [key])		#delete from followers timeline
	d = op.get('FAVORITE_IS', tweetid)					#delete from favourites list
	op.remove_row('FAVORITE_IS', tweetid)
	print d	
	for key in d:
		v = str(d[key])
		op.remove_column('FAVORITE_OF',key,[v])

def is_favourite(uid,tid):
	"check if tweet has already been marked as favourite"
	d = op.get('FAVORITE_OF', uid)
	values = d.values()
	if tid in values:
		return True
	else:
		return False
