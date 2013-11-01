#!/bin/python

import time

def addUser(emailid, username, pwd) :
	"add a user to the network"
	value = {'uid':emailid, 'username':username, 'password':pwd}	
	insert('USERS', emailid, value)


def addFollowers(followerID, followingID) :
	"follower and following a user"
	
	t = long(time.time() * 1e6)
	value = {followingID: t}	
	insert('FOLLOWER', followerID, value)

	value = {followerID: t}	
	insert('FOLLOWING', followingID, value)


def getFollower(uid) :
	"list of users followed by uid"
		
	
def getFollowing(uid) :
	"list of users following uid"
