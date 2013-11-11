#!/usr/bin/python
from flask import Flask,request,jsonify
import operations as op

def get_userline(uid):
        "userline of the user"
        d = op.get_reverse('USERLINE', uid)
	print d
	values = d.values()
	print "VALUES : ", values
	tweets = op.multi_get('TWEETS',values)
	print tweets
	return tweets, values

def get_reply(tid):
	d = op.get('REPLY_TO_TWEET', tid)
	replies = d.values()
	reply_dict=[]
	for t in replies:
		tweet = op.get('TWEETS',t)
		reply_dict[t] = tweet

	return jsonify(reply_dict)

def get_favourite(uid):
	"favourites of a user"
	d = op.get_reverse('FAVORITE_OF', uid)
	print "favorrite of : ", uid, d
	values = d.values()
	tweets = op.multi_get('TWEETS',values)
	print tweets
	return tweets, values	
	 
	
