from flask import Flask, render_template, request, escape, session
from vsearch import search4letters
from DBcm import UseDatabase, ConnectorError, CredentialError, SQLError
from checker import check_logged_in

app = Flask(__name__)

app.secret_key = 'YouWillNeverGuessMySecretKey'

app.config['dbconfig'] = {'host': '127.0.0.1',
			'user':'loh',
			'password':'loh',
			'database':'vsearchlogDB',	}

def log_request(req:'flask request', res:str) -> None:

	with UseDatabase(app.config['dbconfig']) as cursor:
		_SQL = """insert into log
		(phrase, letters, ip, browser_string,results)
		values
		(%s, %s, %s, %s, %s)"""
		cursor.execute(_SQL, (req.form['phrase'],
							req.form['letters'],
							req.remote_addr,
							req.user_agent.browser,
							res, ))
		
@app.route('/search4',methods = ['POST'])
def do_search() ->'html':
	phrase = request.form['phrase']
	letters = request.form['letters']
	title = 'Here are your results'
	results = str(search4letters(phrase, letters))
	try:
		log_request(request,results)
	except Exception as err:
		print('*****Login failed with this error', str(err))
	return render_template('results.html', the_title=title, the_phrase = phrase, the_letters = letters, the_results = results)

@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
	try:
		with UseDatabase(app.config['dbconfig']) as cursor:
			_SQL = """select phrase, letters, ip, browser_string, results from vsearchlogDB.log"""
			cursor.execute(_SQL)
			contents = cursor.fetchall()
		titles = ('Phrase','Letters','Remote_addr','User_agent', 'Results')
		return render_template('viewlog.html', the_title='View Log', the_row_titles = titles, the_data= contents,)
	except Exception as err:
		print('не могу подключиться к бд', str(err))
	except ConnectionError as err:
		print('is your database switched on?', str(err))
	except SQLError as err:
		print ('Is your query correct?', str(err))
	except CredentialError as err:
		print('user-id?password?', str(err))
	return 'Error'

@app.route('/login')
def do_login():
	session['logged_in'] = True
	return 'You are loggin in'

@app.route('/logout')
def do_logout():
	session.pop('logged_in')
	return 'You are now logout'

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
	return render_template('entry.html', the_title='Welcome to search4letters on the web')
if __name__=='__main__':
	app.run(debug=True)