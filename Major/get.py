#!/usr/bin/python
from flask import Flask,request,jsonify
import operations as op

def get_userline(uid):
        "userline of the user"
        d = op.get_reverse('USERLINE', uid)
#	print d
	values = d.values()
#	print "VALUES : ", values
	tweets = op.multi_get('TWEETS',values)
#	print tweets
	return tweets, values

def get_timeline(uid):
        "timeline of the user"
        d = op.get_reverse('TIMELINE', uid)
	if 'status' not in d.keys():
		values = []
		for val in d.values():
			if val!=0:
				values.append(val.split("!")[0])
	
		tweets = op.multi_get('TWEETS',values)
		return tweets, d.values()
	else:	
		return {},[]

def get_reply(tid):
	d = op.get('REPLY_TO_TWEET', tid)
	replies = d.values()
	tweets = op.multi_get('TWEETS',replies)
	original_tweet = op.get('TWEETS',tid)
	return tweets, replies, original_tweet

def get_favourite(uid):
	"favourites of a user"
	d = op.get_reverse('FAVORITE_OF', uid)
#	print "favorrite of : ", uid, d
	values = d.values()
	tweets = op.multi_get('TWEETS',values)
#	print tweets
	return tweets, values	

def get_people(val,uid): 
	"get people" 
	d = op.get('FOLLOWING',uid)
	result1 = {}
	if 'status' not in d.keys():
		e = op.multi_get('USERS',d.keys())
		for k in e.keys():	 
			if e[k]['username'].lower().find(val.lower()) != -1:
				result1[k] = e[k]['username']

	d = op.get_all('USERNAME') 
	result = {} 
	for k,v in d:	 
		if k.lower().find(val.lower()) != -1:
			if v['uid'] not in result1:
				result[v['uid']] = k
	return result1,result


def get_topic(val): 
	"get topic" 
	d = op.get_all('HASH_TAGS') 
	result = {} 
	for k,v in d:	 
		if k.lower().find(val.lower()) != -1:
#			print k, v , v['uid'] 
			result[k] = v
	return result

def get_timeline_count(uid):
	"get number of tweets on timeline"
	d = op.get_count('TIMELINE',uid)
	return d

def get_retweets(uid):
	"get retweets of a user"
	d = op.get('RETWEET',uid)
	return d

def get_userinfo(uid):
	"get users info"
	l = []
	l.append(op.get_count('USERLINE',uid))
	l.append(op.get_count('FOLLOWER',uid))
	l.append(op.get_count('FOLLOWING',uid))
	return l

def get_trendTweets(topicid):
	"get tweets for a topic"
        d = op.get_reverse('HASH_TAGS', topicid)
#	print d
	values = d.values()
#	print "VALUES : ", values
	tweets = op.multi_get('TWEETS',values)
#	print tweets
	return tweets, values

