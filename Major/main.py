#!/usr/bin/python
#!/flask/bin/python
from flask import Flask, request, jsonify,render_template, redirect, url_for, escape, session

import collections 
import time
import uuid
import operations as op
import tweets
import get
import users

app = Flask(__name__)
@app.route('/post',methods=['POST', 'GET'])
def post():
	d={}
	if request.method == 'POST':
		if 'username' in session:
			body = request.form['tweetid']
			uid = session['emailid']			### change to session	
			tweets.post_tweet(body,uid)
			return redirect(url_for('get_userline'))
        return render_template('tweets.html',d=d,username=['username'],other_user=session['other_user'])

@app.route('/tweets',methods=['GET','POST'])
def get_userline():
	d={}
	follow_flag =0
	if 'username' not in session or session['username'] is None:
		return render_template('login.html')
	if request.method == 'GET':
		if session['username']!=session['other_user']:
			follow_flag = users.check_follow(session['other_user'],session['username'])
			val=op.get('USERNAME',session['other_user'])
			uid=val['uid']
		else:
			uid = session['emailid']
		if uid is not None:
			d,l=get.get_userline(uid)
			d1,l1=get.get_favourite(session['emailid'])
			d2=get.get_retweets(session['emailid'])
			return render_template('tweets.html',follow_flag=follow_flag,d=d, l=l, f=l1,username=session['username'], other_user=session['other_user'], retweet=d2)
		else:
			return render_template('login.html')
@app.route('/me',methods=['GET']) 
def me(): 
	session['other_user']=session['username'] 
	session['other_email']=session['emailid'] 
	return redirect(url_for('get_userline'))	


@app.route('/get_reply',methods=['GET'])
def get_reply():
	tid = request.args.get('tid')
	d,l = get.get_reply(tid)
	return jsonify({'data':1})



@app.route('/follow',methods=['GET','POST'])
def follow():
	follower = session['other_user']
	following = session['username']
	followerId = op.get('USERNAME',follower)
	followingId = op.get('USERNAME',following)
	val = users.addFollowers(followerId['uid'],followingId['uid'])
	return redirect(url_for('get_userline'))

@app.route('/unfollow',methods=['GET','POST'])
def unfollow():
	"inside unfollow"
	follower = session['other_user']
	following = session['username']
	followerId = op.get('USERNAME',follower)
	followingId = op.get('USERNAME',following)
	d = op.get('FOLLOWING',followingId['uid'])
	uid1 = followerId['uid']
	uid2 = followingId['uid']
	op.remove_column('FOLLOWING',followingId['uid'],[uid1])
	t = op.get('FOLLOWER',followerId['uid'])
	op.remove_column('FOLLOWER',followerId['uid'],[uid2])
	d = op.get('TIMELINE',uid2)
        for key,value in d.iteritems():
                val = op.get('TWEETS',value)
                if 'status' not in val:
                        if val['user'] == str(uid1):
                                t = str(val['timestamp']) + ":" + uid1
                                op.remove_column('TIMELINE',uid2,[t])
	return redirect(url_for('get_userline'))	

@app.route('/checkfollow',methods=['GET','POST'])
def check_follow():
	follower = session['other_user']
	following = session['username']
	followerId = op.get('USERNAME',follower)
	followingId = op.get('USERNAME',following)
	val = op.get('FOLLOWING',followingId)
	l=val.keys()
	if followerId in l:
		return redirect(url_for('get_userline',follow_flag=1))
	else:
		return redirect(url_for('get_userline',follow_flag=0))


@app.route('/home',methods=['POST', 'GET']) 
def home(): 
	startval = request.args.get('start')
	startval = int(startval)
	session['tweet_count']=get.get_timeline_count(session['emailid'])
	session['other_user']=session['username'] 
	session['other_email']=session['emailid'] 
	uid = session['emailid'] 
	info = get.get_userinfo(uid) 
	d,l = get.get_timeline(uid) 
	d2 = get.get_retweets(session['emailid'])
	d1,l1=get.get_favourite(session['emailid'])
	current_trends = tweets.current_trends()
	if (len(l) > startval + 5) :
		limit = startval + 5
		nextt = limit
	else :
		limit=len(l)
		nextt = 0

	l=l[startval:limit]
	if(startval==0):
		return render_template('home.html',info=info, d=d, l=l, retweet=d2, f=l1, start=int(nextt), trends= current_trends)
	else:
		return jsonify ({'d':d,'l':l,'retweet':d2,'f':l1,'start':nextt, 'trends':current_trends})	

@app.route('/index')
def index():
	if 'username' in session:
		return 'Hello %s' % escape(session['username'])
	return 'You are not logged in'


@app.route('/login',methods=['POST','GET'])
def login():
	if 'emailid' in session:
		return redirect(url_for('get_userline'))
	if request.method == 'POST':
		
		email = request.form['emailid']
		pwd = request.form['password']
		val=users.checkUser(email,pwd)
		if val!=str(0):	
			session['username']=val
			session['emailid'] = request.form['emailid']
			session['other_user']=session['username']
			session['other_email']=session['emailid']
			session['tweet_count']=get.get_timeline_count(session['emailid'])
		else:
		 	message="Incorrect password or username"
		 	return render_template('login.html',message=message)
		return redirect(url_for('get_userline'))
	else:
		return render_template('login.html',message="")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if 'emailid' in session:
		return redirect(url_for('get_userline'))
	if request.method == 'POST':
		email = request.form['emailid']
		username = request.form['username']
		pwd = request.form['password']
		check_pwd = request.form['check_password']
		if pwd!=check_pwd:
			message = "enter correct password"
			return render_template('signup.html',message=message)
		else:
			val = users.user_exist(email,username)
			if val!=str(0):				
				users.addUser(email,username,pwd)
				session['emailid'] = request.form['emailid']
				session['username']=request.form['username']
				session['other_user']=session['username']
				session['other_email']=session['emailid']
	       			return redirect(url_for('get_userline'))
			else:
				message="Username or emailid already exists"
				return render_template('signup.html',message=message)
	else:
		return render_template('signup.html',message="")

@app.route('/following',methods=['GET','POST'])
def following():
	other_uid = op.get('USERNAME',session['other_user'])
	d = op.get('FOLLOWING',other_uid['uid'])
	d1={}
	if not(d.has_key('status')):
		for uid in d.iterkeys():
			val = op.get('USERS',uid)
			d1[uid] = val['username']
	return render_template('following.html',d=d1,username=session['username'],other_user=session['other_user'])

@app.route('/followers',methods=['GET','POST'])
def followers():
	other_uid = op.get('USERNAME',session['other_user'])
	d = op.get('FOLLOWER',other_uid['uid'])
	d1={}
	if not(d.has_key('status')):
		for uid in d.iterkeys():
			val = op.get('USERS',uid)
			d1[uid] = val['username']
	return render_template('followers.html',d=d1,username=session['username'],other_user=session['other_user'])

@app.route('/favourite',methods=['GET'])
def favourite():
	tweetid = request.args.get('id')
	uid = session['emailid']
	tweets.mark_as_favorite(uid,tweetid)
	session['other_user'] = session['username']
	session['other_email'] = session['emailid']
	return redirect(url_for('myfavourites'))


@app.route('/myfavourites',methods=['GET'])
def myfavourites():
	user = session['other_user']
	val = op.get('USERNAME',user);
	uid = val['uid'] 
	d,l=get.get_favourite(uid)
#	session['other_user'] = session['username']
	return render_template('favourite.html',d=d, l=l, username=session['username'], other_user = session['other_user'])


@app.route('/delete',methods=['GET'])
def delete():
	tweetid = request.args.get('id')
	prev = request.args.get('prev')
	uid = session['emailid']
	tweets.delete_tweet(tweetid,uid)
	return redirect(url_for(prev))

@app.route('/post_reply',methods=['POST', 'GET'])
def post_reply():
	d={}
	if request.method == 'POST':
		if 'username' in session:
			body = request.form['repid']
			tid = request.form['tid']
			uid = session['emailid']			### change to session	
			tweets.post_reply(tid,uid,body)
			return redirect(url_for('get_userline'))
	else:
		print "jk"
        return render_template('tweets.html',d=d,username=session['username'],other_user=session['other_user'])


@app.route('/signup_page',methods=['POST', 'GET'])
def signup_page():
        return render_template('signup.html')

@app.route('/search_page',methods=['POST', 'GET']) 
def search_page(): 
	return render_template('search.html',username = session['username'], other_user = session['other_user'])

@app.route('/set_other_user',methods=['POST', 'GET']) 
def set_other_user(): 
	session['other_user']=request.args.get('user') 
	session['other_email']=request.args.get('email') 
	return redirect(url_for('get_userline'))

@app.route('/search',methods=['POST', 'GET']) 
def search(): 
	if request.method == 'POST': 
		if 'username' in session:
			val = request.form['searchtext'] 
			typeof = request.form['searchtype'] 
			if typeof == 'people':
				d,e = get.get_people(val,session['emailid'])
				return render_template('search.html',d=d, e=e, req='people')
			else:
				t = get.get_topic(val)
				return render_template('search.html',t=t, req='topic')
		else :
			return render_template('login.html')
	else: 
		print "GET TYPE"

@app.route('/read_thread',methods=['POST', 'GET'])
def read_thread():
	tid = request.args.get('id')
#	tid = get.get_super_tweetID(tweetid)
	d,l,t = get.get_reply(tid)
	return jsonify({'d':d, 'l':l, 't':t})


@app.route('/logout',methods=['POST', 'GET']) 
def logout(): 
	session.pop('username', None)
	session.pop('emailid', None)
	session.pop('other_user', None)
	session.pop('other_email', None)
	session.pop('tweet_count',None)
	return render_template('login.html',message="")


@app.route('/notification',methods=['POST', 'GET'])
def notification():
	"notification method called"
	count = get.get_timeline_count(session['emailid'])
	diff = count - session['tweet_count']
	if diff <0:
		session['tweet_count']=count
	return jsonify({'count':diff})

@app.route('/untweet',methods=['POST', 'GET'])
def untweet():
	"untweet method called"
	tid = request.args.get('tid')
	tweets.untweet(tid,session['emailid'])
	return redirect(url_for('get_userline'))

@app.route('/retweet',methods=['POST', 'GET'])
def retweet():
	"untweet method called"
	tid = request.args.get('tid')
	tweets.retweet(tid,session['emailid'])
	return redirect(url_for('get_userline'))

@app.route('/show_trends',methods=['POST', 'GET'])
def show_trends():
	"show_trends method called"
	topicid = request.args.get('topic')
	d,l = get.get_trendTweets(topicid)
	d1,l1=get.get_favourite(session['emailid'])
	d2=get.get_retweets(session['emailid'])
	return render_template('trends.html',d=d,l=l,f=l1,retweet=d2)

if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host = '192.168.43.189',debug=True)
#	app.run(host = '10.1.98.237',debug=True)

