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
		op.insert('USERS', emailid, value)
		op.insert('USERNAME', username, {'uid':emailid})
		print emailid 
		print value
	except:
		print "exception"
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
        
        t = long(time.time() * 1e6)
        value = {followingID: t}        
	try:
		op.insert('FOLLOWER', followerID, value)

        	value = {followerID: t}        
        	op.insert('FOLLOWING', followingID, value)
	except:
		return 0
	return 1

def getFollower(uid) :
        "list of users followed by uid"
                
        
def getFollowing(uid) :
        "list of users following uid"


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
		print "inside exception"
		return 0
	return 1
