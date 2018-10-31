from flask import Flask, session
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'YouWillNeverGuessMySecretKey'

@app.route('/')
def hello():
	return 'Hello from the simple app'

@app.route('/page1')
@check_logged_in
def page1():
	return 'This is page1'

@app.route('/page2')
@check_logged_in
def page2():
	return 'This is page2'

@app.route('/page3')
@check_logged_in
def page3():
	return 'This is page3'

@app.route('/login')
def do_login():
	session['logged_in'] = True
	return 'You are loggin in'

@app.route('/logout')
def do_logout():
	session.pop('logged_in')
	return 'You are now logout'

if __name__=='__main__':
	app.run(debug=True)