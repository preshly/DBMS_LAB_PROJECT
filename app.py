
from flask import Flask, render_template, request, session, redirect
import config
from dbcm import Usedatabase

#define the app
app = Flask(__name__)

#secret key for the app to maintain session cookies
app.secret_key = config.secret_key

app.config['UPLOADED_PHOTOS'] = 'static/products'

#database configurations for the app
app.config['dbconfig'] = config.dbconfig


@app.route('/')
@app.route('/home')
def website() -> 'html':
	"""
	Output: Home page for the website.
	Display the page with products, sign-up link and log-in link.
	Select 4 products from the different range of product from each category available in the database.

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
	
	#return render_template('website.html', smartphone = smartphone, earphone = earphone, tshirt = tshirt)
	return render_template('website.html', products = products)

@app.route('/signup')
def signup() -> 'html':
	"""
	Output: signup page for the customer.
	Display the sign up form for the new customers.
	"""
	return render_template('signup.html')

@app.route('/customer_login')
def customer_login() -> 'html':
	"""
	Output: login page for the customer.
	Display the log in form  for the existing customers.
	"""
	return render_template('customer_login.html')

@app.route('/admin_login')
def admin_login() -> 'html':
	"""
	Output: login page for the admin.
	Display the log in form  for the admin of the website.
	"""
	return render_template('admin_login.html')

@app.route('/my_account')
def my_account() -> 'html':
	"""
	Output: The details of the customer.
	"""
	return render_template('my_account.html')

#run the app
if __name__ == '__main__':
	app.run(debug = True)
