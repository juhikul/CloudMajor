#!/bin/python
#!/flask/bin/python
from flask import Flask, jsonify
import time
import operations as op

def addUser(emailid, username, pwd) :
        "add a user to the network"
	print "add user function"
        value = {'uid':emailid, 'username':username, 'password':pwd}        
	try:
		print emailid, value, username
		op.insert('USERS', emailid, value)
		val={'uid':emailid}
		op.insert('USERNAME', username, val)
	except:
		print "inside execp"
		return 0
	return 1

def checkUser(emailid,pwd):
	value = op.get('USERS',emailid)
	if 'status' in value:
		return str(0)
	if value['password']==pwd:
		return value['username']
	else:
		return str(0)

def user_exist(emailid,username):
	value1 = op.get('USERS',emailid)
	value2 = op.get('USERNAME',username)
	if 'status' in value1 or 'status' in value2:
		return str(1)
	else :
		return str(0)

def addFollowers(followerID, followingID) :
        "follower and following a user"
        t = str(long(time.time() * 1e6))
        value = {followingID: t}        
	try:
		op.insert('FOLLOWER', followerID, value)
        	value = {followerID: t}        
        	op.insert('FOLLOWING', followingID, value)
		val = op.get('USERLINE',followerID)
                op.insert('TIMELINE',followingID,val)
	except:
		return 0
	return 1

def check_follow(follower,following):
        followerId = op.get('USERNAME',follower)
        followingId = op.get('USERNAME',following)
        val = op.get('FOLLOWING',followingId['uid'])
        l=val.keys()
        if followerId['uid'] in l:
                return 1
        else:
                return 0


def login(uid, password) :
	"check if a user is valid"
	print "inside login"
	try:
        	d = op.get('USERS', uid)
		if (d['password'] == password) :
			return 1
		else :
			return 2
	except:
		return 0
	return 1
