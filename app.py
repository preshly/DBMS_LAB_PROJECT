
from flask import Flask, render_template, request, session, redirect, url_for, flash
import config
from dbcm import Usedatabase
from passlib.hash import mysql41
from checker import is_customer_logged_in
#from forms import Customer_Signup

#define the app
app = Flask(__name__)

#secret key for the app to maintain session cookies
app.secret_key = config.secret_key

#app.config['UPLOADED_PHOTOS'] = 'static/products'

#database configurations for the app
app.config['dbconfig'] = config.dbconfig



def insert_customer_to_db(user_details: list) -> None:
	"""
	function to enter the cunstomer details in the DB
	input: userDetails as a list of values. Use the list elemenst to add to the customer table in the DB
	output: None
	"""
	with Usedatabase(app.config['dbconfig']) as cursor:
			_SQL = """insert into customer 
					(email, firstName, lastName, contact, houseNoOrFlatNo, streetOrvillage, cityOrTown, state, country, username, password)
					values
					(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
					"""
			cursor.execute(_SQL, (user_details[0], user_details[1], user_details[2], user_details[3], user_details[4], user_details[5], user_details[6], user_details[7], user_details[8], user_details[9], user_details[10] ) )

def get_cutomer_id_from_db(username: str, email: str) -> int:
	"""
	function to get the user id from the DB, with the input as username and email
	input: username, email. This is used to find the userid with the corresponding username and email
	output: int(userID) if exists, else None
	"""
	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """select idCustomer from customer where email=%s and username=%s; """
		cursor.execute(_SQL, (email, username) )
		idCustomer = cursor.fetchone()
		if int(idCustomer[0]) > 0:
			return int(idCustomer[0])
		else:
			return None

def set_userid_to_flask_app_config(username: str, email: str, password: str) -> None:
	"""
	function to set the userid of the loggedin customer to the app.config
	input: username, email. This is used to find the userid with the corresponding username and email
	output: None
	"""
	idCustomer = get_cutomer_id_from_db(username, email)

	#app.config['loggged_userid']
	#app.config['loggged_username']
	#app.config['logged_userpassword']



	if idCustomer != None:
		#app.config['loggged_userid'] = idCustomer
		#app.config['loggged_username'] = username
		#app.config['logged_userpassword'] = password
		session['customer_logged_in'] = True
		session['customer_id'] = idCustomer
		session['customer_username'] = username
		session['customer_email'] = email
		session['customer_password'] = password
		#print( app.config['loggged_userid'], app.config['loggged_username'] )


@app.route('/')
def website() -> 'html':
	"""
	Output: Home page for the website.
	Display the page with products, sign-up link and log-in link.
	Select 4 products from the different range of product from each category available in the database.

	"""
	messages = []
	with Usedatabase(app.config['dbconfig']) as cursor:
		products = dict()
		_SQL = """select image, name, cost from product where categoryName = 'smartphone' order by rand() limit 4; """
		cursor.execute(_SQL)
		#smartphone = cursor.fetchall()
		products['smartphone'] = cursor.fetchall()

		_SQL = """select image, name, cost from product where categoryName = 'earphones' order by rand() limit 4; """
		cursor.execute(_SQL)
		#earphones = cursor.fetchall()
		products['earphones'] = cursor.fetchall()

		_SQL = """select image, name, cost from product where categoryName = 'tshirt' order by rand() limit 4; """
		cursor.execute(_SQL)
		#tshirt = cursor.fetchall()
		products['tshirt'] = cursor.fetchall()
	
	#return render_template('website.html', smartphone = smartphone, earphone = earphone, tshirt = tshirt)
	return render_template('website.html', products = products, messages = messages)

@app.route('/signup', methods=['GET', 'POST'])
#@is_customer_logged_in
def signup() -> 'html':
	"""
	Output: signup page for the customer.
	Display the sign up form for the new customers.
	"""
	#customer_signup_form = Customer_Signup(request.form.get(), csrf_enabled=False)
	#if customer_signup_form.validate_on_submit():
	messages = []
	if request.method == 'POST':
		firstName = request.form['firstname']
		lastName = request.form['lastname']
		email = request.form['email']
		contact = request.form['contact']
		houseNO = request.form['houseno']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		username = request.form['username']
		password = request.form['password']

		userDetails = [email, firstName, lastName, str(contact), houseNO, street, city, state, country, username, password]

		for value in userDetails:
			if not value:
				#flash('Please fill all the details')
				messages = ['Please fill all the details']
				return render_template('signup.html', messages = messages)

		#try:
		hash_password = mysql41.hash(password)
		userDetails.remove(password)
		userDetails.append(str(hash_password))
		"""
		except Exception:
			flash('Please fill all the details ')
			return render_template('signup.html')
		"""

		#print(firstName, lastName, email, contact, houseNO, street, city, state, country)
		#print(firstName, username, password, hash_password)
				
		with Usedatabase(app.config['dbconfig']) as cursor:
			#customers = dict()
			_SQL = """select email from customer; """
			cursor.execute(_SQL)
			emailsDB = cursor.fetchall()
			#print(emailsDB)
			#print(email in emailsDB)

			_SQL = """select username from customer; """
			cursor.execute(_SQL)
			usernamesDB = cursor.fetchall()
			#print(usernamesDB)
			#print(username in usernamesDB)

			for un in usernamesDB:
				#print(username == un[0])
				if username == un[0]:					
					#flash('Username or Email already taken')
					messages = ['Username or Email already taken'] 
					return render_template('signup.html', messages = messages)
			
			for em in emailsDB:
				#print(email, em)
				if email == em[0]:
					#flash('Username or Email already taken')
					messages = ['Username or Email already taken'] 
					return render_template('signup.html', messages = messages)

		insert_customer_to_db(userDetails)
		
		set_userid_to_flask_app_config(username, email, password)
		#print( app.config['loggged_userid'], app.config['loggged_username'] )

		flash('Signup successful')
		#messages = ['Signup successful']
		return redirect(url_for('customer_loggedin_home_page' ))

	return render_template('signup.html', messages = messages)

@app.route('/customer_login', methods=['GET', 'POST'])
#@is_customer_logged_in
def customer_login() -> 'html':
	"""
	Output: login page for the customer.
	Display the log in form  for the existing customers.
	"""
	messages = []
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		userDetails = [username, password]

		for value in userDetails:
			if not value:
				#flash('Please fill all the details')
				messages = ['Please fill all the details']
				return render_template('customer_login.html', messages=messages)
		
		with Usedatabase(app.config['dbconfig']) as cursor:
				_SQL = """select username, password, email from customer; """
				cursor.execute(_SQL)
				loginDetailsDB = cursor.fetchall()

				for un in loginDetailsDB:
					#print(username == un[0])
					if username == un[0]:					
						#flash('Username or Email already taken')
						if mysql41.verify(password, un[1]):						
							flash('Login successful')
							#messages = ['Login Successful']

							set_userid_to_flask_app_config(un[0], un[2], password)

							#print('login succes')

							#print(session['customer_username'], session['customer_id'])
							#print(session['customer_username'], session['customer_id'], session['customer_username'], session['customer_password'])
							#print(type(app.config['loggged_userid']))
							#print( app.config['loggged_userid'], app.config['loggged_username'] )
							return redirect(url_for('customer_loggedin_home_page'))
			
			
				#flash('Invalid username or password')
				messages = ['Invalid username or password']
	return render_template('customer_login.html', messages=messages)


@app.route('/customer_logout')
def customer_logout():
	if 'customer_logged_in' in session:
		#session.clear()
		session.pop('customer_logged_in')
		session.pop('customer_id')
		session.pop('customer_username')
		session.pop('customer_email')
		session.pop('customer_password')
		flash('You are logged out')
		#messages = ['You are logged out']
		return redirect(url_for('website') )
	return redirect(url_for('customer_login'))

@app.route('/home')
def customer_loggedin_home_page() -> 'html':
	"""
	Output: display home page when customer is logged in
	This method is called only when the customer is logged in to the website
	"""
	with Usedatabase(app.config['dbconfig']) as cursor:
		products = dict()
		_SQL = """select image, name, cost from product where categoryName = 'smartphone' order by rand() limit 4; """
		cursor.execute(_SQL)
		#smartphone = cursor.fetchall()
		products['smartphone'] = cursor.fetchall()

		_SQL = """select image, name, cost from product where categoryName = 'earphones' order by rand() limit 4; """
		cursor.execute(_SQL)
		#earphones = cursor.fetchall()
		products['earphones'] = cursor.fetchall()

		_SQL = """select image, name, cost from product where categoryName = 'tshirt' order by rand() limit 4; """
		cursor.execute(_SQL)
		#tshirt = cursor.fetchall()
		products['tshirt'] = cursor.fetchall()
	
	return render_template('customer_loggedin_home_page.html', products = products)

@app.route('/my_account')
@is_customer_logged_in
def my_account() -> 'html':
	"""
	Output: The details of the customer.
	"""
	userDetailsList = []

	customerUsername = session['customer_username']
	customerEmail = session['customer_email']
	
	if 'customer_logged_in' in session:	
		with Usedatabase(app.config['dbconfig']) as cursor:
			#_SQL = """select firstName, lastName, email, contact, houseNoOrFlatNo, streetOrvillage, cityOrTown, state, country, username from customer where username=%s; """
			_SQL = """select firstName, lastName, email, contact, houseNoOrFlatNo, streetOrvillage, cityOrTown, state, country, username from customer where email=%s and username=%s; """
			#cursor.execute(_SQL, ( session['customer_id'] ))
			cursor.execute(_SQL, (customerEmail, customerUsername))
			#session['customer_username']
			userDetails = cursor.fetchone()

			userDetailsList = list(userDetails)
			userDetailsList.append(session['customer_password'])


	return render_template('my_account.html', userDetails = userDetailsList)


@app.route('/admin_login')
def admin_login() -> 'html':
	"""
	Output: login page for the admin.
	Display the log in form  for the admin of the website.
	"""
	return render_template('admin_login.html')



#run the app
if __name__ == '__main__':
	app.run(debug = True)
