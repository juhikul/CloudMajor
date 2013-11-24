#!/usr/bin/python
#!/flask/bin/python
from flask import Flask, request, jsonify

import time
import uuid
import operations as op
import operator

app = Flask(__name__)

def check_for_hashtag(body,t,timestamp):
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
		op.insert('TIMELINE',value['uid'],{timestamp:t})

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
#       op.insert('TIMELINE', uid, {timestamp:t})
	parse(t,uid)
	for followerID in op.get('FOLLOWER', uid):
		if 'status' != followerID:
               	   op.insert('TIMELINE', followerID, {timestamp:t})		#DO
	
	return jsonify({'tid':t,'body':msg,'user':uid})

def mark_as_favorite(uid,tid):
	val = is_favourite(uid,tid)
	if val:
		d = op.get('FAVORITE_IS', tid)
		t = d[uid]
		op.remove_column('FAVORITE_OF', uid,[t])
		op.remove_column('FAVORITE_IS', tid,[uid])		
	else:
		val = op.get('TWEETS',tid)
		timestamp = long(time.time() * 1e6)
		timestamp = str(timestamp)
		op.insert('FAVORITE_OF', uid, {timestamp:tid})
		op.insert('FAVORITE_IS', tid, {uid:timestamp})
	

def post_reply(tid, uid, msg) :
        "reply to a tweet"
        t = str(uuid.uuid4())
        timestamp = long(time.time() * 1e6)
        timestamp = str(timestamp)	
        value = {'body':msg, 'user':uid, 'timestamp':timestamp}
        op.insert('TWEETS', t, value)
	timestamp = timestamp + ":" + uid
        op.insert('REPLY_TO_TWEET', tid, {timestamp:t})
	op.insert('USERLINE',uid, {timestamp:t})
	for followerID in op.get('FOLLOWER', uid):
		if 'status' != followerID:
               	   op.insert('TIMELINE', followerID, {timestamp:t})		#DO


def delete_tweet(tweetid,uid) :
	"to delete a tweet"
	val = op.get('TWEETS',tweetid)
	op.remove_row('TWEETS', tweetid)
	key = str(val['timestamp']) + ":" + uid
	op.remove_column('USERLINE', uid, [key])				#delete from timeline and userline
	op.remove_column('TIMELINE', uid, [key])
	print "during delete " + key
	for followerID in op.get('FOLLOWER', uid):
		print followerID
		if 'status' != followerID:
			op.remove_column('TIMELINE', followerID, [key])		#delete from followers timeline

	d = op.get('FAVORITE_IS', tweetid)					#delete from favourites list
	op.remove_row('FAVORITE_IS', tweetid)
	for key in d:
		v = str(d[key])
		op.remove_column('FAVORITE_OF',key,[v])
	d = op.get_all('HASH_TAGS')
        for k,v in d:
                for key,val in v.items():
                        if 'status' != key:
                                if str(tweetid) == str(val):
                                        op.remove_column('HASH_TAGS',k,[key])

def is_favourite(uid,tid):
	"check if tweet has already been marked as favourite"
	d = op.get('FAVORITE_OF', uid)
	values = d.values()
	if tid in values:
		return True
	else:
		return False


def retweet(tid, uid):
	"retweet an existing tweet"
        timestamp = long(time.time() * 1e6)
	timestamp = str(timestamp) + ":" + str(uid)	
	t = str(uuid.uuid4())

	d = op.get('TWEETS',tid)
        value = {'body':d['body'], 'user':d['user'], 'timestamp':str(timestamp)}
        op.insert('TWEETS', t, value)

	op.insert('USERLINE', uid, {timestamp:t})
	op.insert('RETWEET', uid, {tid:t})
	print "retweeting"
	for followerID in op.get('FOLLOWER', uid):
		print followerID
		if 'status' != followerID:
			tweet=str(t)+"!"+str(uid)
			op.insert('TIMELINE', followerID, {timestamp:tweet})		#DO

def untweet(tid, uid):
	"untweet a retweeted tweet"
	
	d = op.get('RETWEET',uid)
	print d
	for k in d.keys():
		if d[k]==tid or k==tid:
			t1,t2 = k,d[k]

	op.remove_column('RETWEET', uid, [t1])
	delete_tweet(t2,uid)

def current_trends():
        print "inside trends"
        etime = long(time.time())
        reference_t = (etime - (etime % 86400)) + time.altzone
#        reference_t = long(midnight) - long(86400*1e6)
        result = op.get_all('HASH_TAGS')
        count={}
        for k,v in result:
                count[k] = 0
                for key,val in v.items():
			print key,val
                        val1 = str(key).split(":")
			print val1[0]
                        timestamp = val1[0]
                        if float(timestamp) >= float(reference_t):
                                count[k] = count[k] + 1
        sorted_trends = sorted(count.iteritems(), key=operator.itemgetter(1),reverse=True)
        current_trends = sorted_trends[:10]
        print current_trends
        return current_trends
