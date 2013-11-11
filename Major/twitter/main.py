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
			print body + ":" + uid
			tweets.post_tweet(body,uid)
			return redirect(url_for('get_userline'))
	else:
		print "jk"
        return render_template('tweets.html',d=d)

@app.route('/tweets',methods=['GET','POST'])
def get_userline():
	d={}
	if request.method == 'GET':
		uid = session['emailid']
#		uid='jk'
		print uid
		d,l=get.get_userline(uid)
		d1,l1=get.get_favourite(uid)
		print d
		return render_template('tweets.html',d=d, l=l, f=l1)

@app.route('/get_reply',methods=['GET'])
def get_reply():
	tid = request.args.get('tid')
	get.get_reply(tid)
	return jsonify({'success':1})



@app.route('/follow',methods=['GET'])
def follow_user():
	followId = request.args.get('followerId')
	followingId = request.args.get('followingId')
	return jsonify({'success':1})


@app.route('/index')
def index():
	if 'username' in session:
		return 'Hello %s' % escape(session['username'])
	return 'You are not logged in'


@app.route('/login',methods=['POST','GET'])
def login():
	if request.method == 'POST':
		
		email = request.form['emailid']
		pwd = request.form['password']
		val=users.checkUser(email,pwd)
		if val!=str(0):	
			session['username']=val
			session['emailid'] = request.form['emailid']
		else:
		 	message="Incorrect password or username"
		 	return render_template('login.html',message=message)
		return redirect(url_for('get_userline'))
	else:
		return render_template('login.html',message="")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['emailid']
		username = request.form['username']
		pwd = request.form['password']
		check_pwd = request.form['check_password']
		if pwd!=check_pwd:
			message = "enter correct password"
			return render_template('signup.html',message=message)
		else:
			print "else part"
			val = users.user_exist(email,username)
			print "check user "+val
			if val!=str(0):				
				users.addUser(email,username,pwd)
				session['emailid'] = request.form['emailid']
				session['username']=request.form['username']
	       			return redirect(url_for('index'))
			else:
				message="Username or emailid already exists"
				return render_template('signup.html',message=message)
	else:
		return render_template('signup.html',message="")


@app.route('/favourite',methods=['GET'])
def favourite():
	tweetid = request.args.get('id')
	uid = session['emailid']
	tweets.mark_as_favorite(uid,tweetid)
	return redirect(url_for('myfavourites'))


@app.route('/myfavourites',methods=['GET'])
def myfavourites():
	uid = request.args.get('user')
	if uid is None:
		print "UID in EXCEPT"
		uid = session['emailid']
	print "GETTING FAV TWEETS FOR USER ", uid
	d,l=get.get_favourite(uid)
	return render_template('favourite.html',d=d, l=l, name=session['emailid'])


@app.route('/delete',methods=['GET'])
def delete():
	tweetid = request.args.get('id')
	prev = request.args.get('prev')
	uid = session['emailid']
	print "DELETEING A TWEET ", uid, "PREVIOUS PAGE", prev
	tweets.delete_tweet(tweetid,uid)
	return redirect(url_for(prev))


if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#	app.run(host = '10.3.3.89',debug=True)
	app.run(host = '10.1.98.237',debug=True)

