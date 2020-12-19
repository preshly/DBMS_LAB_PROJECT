
from flask import Flask, render_template, request, session, redirect, url_for, flash
import config
from dbcm import Usedatabase
from passlib.hash import mysql41
from checker import is_customer_logged_in, is_admin_logged_in
import mysql

"""
Initialize and set the secret key for the app.
Also initialize the database configurations to app.config
"""
#define the app
app = Flask(__name__)

#secret key for the app to maintain session cookies
app.secret_key = config.secret_key

#database configurations for the app
app.config['dbconfig'] = config.dbconfig


"""
Below are the functions that are used in the methods for customers and the admin
"""
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
	function to set the userid of the loggedin customer to the session
	input: username, email. This is used to find the userid with the corresponding username and email
	output: None
	"""
	idCustomer = get_cutomer_id_from_db(username, email)

	if idCustomer != None:
		session['customer_logged_in'] = True
		session['customer_id'] = idCustomer
		session['customer_username'] = username
		session['customer_email'] = email
		session['customer_password'] = password

def get_admin_id_from_db(username: str, email: str) -> int:
	"""
	function to get the admin id from the DB, with the input as username and email
	input: username, email. This is used to find the admin id with the corresponding username and email
	output: int(userID) if exists, else None
	"""
	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """select idAdmin from admin where email=%s and username=%s; """
		cursor.execute(_SQL, (email, username) )
		idAdmin = cursor.fetchone()
		if int(idAdmin[0]) > 0:
			return int(idAdmin[0])
		else:
			return None

def set_adminid_to_flask_app_config(username: str, email: str, password: str) -> None:
	"""
	function to set the admin id of the loggedin admin to the session
	input: username, email. This is used to find the userid with the corresponding username and email
	output: None
	"""
	idCustomer = get_admin_id_from_db(username, email)

	if idCustomer != None:
		session['admin_logged_in'] = True
		session['admin_id'] = idCustomer
		session['admin_username'] = username
		session['admin_email'] = email
		session['admin_password'] = password
		#print(session['admin_id'])

"""
Below are all the methods that are related to teh customers of the website
"""
@app.route('/')
def website() -> 'html':
	"""
	Output: Home page for the website.
	Display the page with products, sign-up link and log-in link.
	Select 4 products from the different range of product from each category available in the database.

	"""
	#messages = []
	with Usedatabase(app.config['dbconfig']) as cursor:
		frequently_viewed_products = dict()
		_SQL = """ select idProduct from cart group by idProduct order by rand() limit 4; """
		cursor.execute(_SQL)
		productIdDB = cursor.fetchall()

		idProductDBList = list()
		for id in productIdDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			idSet = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, idSet)
			frequently_viewed_products[id] = cursor.fetchall()
		
		recently_ordered_products = dict()
		_SQL = """ select idProduct from orders group by idProduct order by rand() limit 4; """
		cursor.execute(_SQL)
		productIdDB = cursor.fetchall()

		idProductDBList = list()
		for id in productIdDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			idSet = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, idSet)
			recently_ordered_products[id] = cursor.fetchall()
		
		_SQL = """ select categoryName from category; """
		cursor.execute(_SQL)
		categoryNameDB = cursor.fetchall()

		categoryNameDBList = list()
		for name in categoryNameDB:
			categoryNameDBList.append(name[0])

		products = dict()
		for name in categoryNameDB:
			_SQL = """select image, name, cost, idProduct from product where categoryName = %s order by rand() limit 4 ; """
			cursor.execute(_SQL, name)
			products[name] = cursor.fetchall()
	
	return render_template('website.html', 
		frequentProducts = frequently_viewed_products, 
		recently_ordered_products = recently_ordered_products,
		products = products)

@app.route('/add_to_cart', methods=['GET', 'POST'])
@is_customer_logged_in
def add_product_to_cart():

	code = int(request.form['code'])
	#price = float(request.form['productPrice'])
	#print(session['customer_id'])
	idCustomer = session['customer_id']
	#print(session['customer_username'])
	#print(code)
	#print(image)
	#print(price)
	#print(quantity)
	#print(request.user_agent.browser)
	#print(request.remote_addr)
	#search_set = (image,)
	#print(search_set)

	idCustomer_search_set = (idCustomer, )
	idCustomer_idProduct_insert_set = (idCustomer, code)

	#messages = []
	with Usedatabase(app.config['dbconfig']) as cursor:
		try:
			_SQL = """select idProduct from cart where idCustomer = %s;  """
			cursor.execute(_SQL, (idCustomer_search_set))
			idProductDB = cursor.fetchall()

			#idProductDBList = list(idProductDB)
			'''
			if code in idProductDBList:
				#flash("Item already present in the cart")
				messages = ["Item already present in the cart"]
			else:
				'''
			_SQL = """insert into cart (idCustomer, idProduct) values(%s, %s);  """
			cursor.execute(_SQL, (idCustomer_idProduct_insert_set))
			flash("Item added to cart")
		except mysql.connector.errors.IntegrityError:
			flash("Item already present in the cart")

	return redirect(url_for('customer_loggedin_home_page'))


@app.route('/signup', methods=['GET', 'POST'])
#@is_customer_logged_in
def signup() -> 'html':
	"""
	Output: signup page for the customer.
	Display the sign up form for the new customers.
	"""
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
				messages = ['Please fill all the details']
				return render_template('signup.html', messages = messages)

		
		hash_password = mysql41.hash(password)
		userDetails.remove(password)
		userDetails.append(str(hash_password))

				
		with Usedatabase(app.config['dbconfig']) as cursor:
			
			_SQL = """select email from customer; """
			cursor.execute(_SQL)
			emailsDB = cursor.fetchall()
			
			_SQL = """select username from customer; """
			cursor.execute(_SQL)
			usernamesDB = cursor.fetchall()

			for un in usernamesDB:
				if username == un[0]:					
					messages = ['Username or Email already taken'] 
					return render_template('signup.html', messages = messages)
			
			for em in emailsDB:
				if email == em[0]:
					messages = ['Username or Email already taken'] 
					return render_template('signup.html', messages = messages)

		insert_customer_to_db(userDetails)
		
		set_userid_to_flask_app_config(username, email, password)
		
		flash('Signup successful')
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
				messages = ['Please fill all the details']
				return render_template('customer_login.html', messages=messages)
		
		with Usedatabase(app.config['dbconfig']) as cursor:
				_SQL = """select username, password, email from customer; """
				cursor.execute(_SQL)
				loginDetailsDB = cursor.fetchall()

				for un in loginDetailsDB:
					if username == un[0]:					
						if mysql41.verify(password, un[1]):						
							flash('Login successful')

							set_userid_to_flask_app_config(un[0], un[2], password)
							
							return redirect(url_for('customer_loggedin_home_page'))
			
				messages = ['Invalid username or password']
	return render_template('customer_login.html', messages=messages)


@app.route('/customer_logout')
def customer_logout():
	if 'customer_logged_in' in session:
		#session.clear()
		#session['customer_logged_in'] = False
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
		frequently_viewed_products = dict()
		_SQL = """ select idProduct from cart group by idProduct order by rand() limit 4; """
		cursor.execute(_SQL)
		productIdDB = cursor.fetchall()

		idProductDBList = list()
		for id in productIdDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			idSet = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, idSet)
			frequently_viewed_products[id] = cursor.fetchall()
		

		recently_ordered_products = dict()
		_SQL = """ select idProduct from orders group by idProduct order by rand() limit 4; """
		cursor.execute(_SQL)
		productIdDB = cursor.fetchall()

		idProductDBList = list()
		for id in productIdDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			idSet = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, idSet)
			recently_ordered_products[id] = cursor.fetchall()

		_SQL = """ select categoryName from category; """
		cursor.execute(_SQL)
		categoryNameDB = cursor.fetchall()

		categoryNameDBList = list()
		for name in categoryNameDB:
			categoryNameDBList.append(name[0])

		products = dict()
		for name in categoryNameDB:
			_SQL = """select image, name, cost, idProduct from product where categoryName = %s order by rand() limit 4 ; """
			cursor.execute(_SQL, name)
			products[name] = cursor.fetchall()
	
	return render_template('customer_loggedin_home_page.html', 
		frequentProducts = frequently_viewed_products, 
		recently_ordered_products = recently_ordered_products,
		products = products)

@app.route('/my_cart')
@is_customer_logged_in
def my_cart() -> 'html':
	"""
	output the products from the user's cart from database to the webpage
	"""
	
	with Usedatabase(app.config['dbconfig']) as cursor:
		idCustomer = session['customer_id']
		idCustomer_search_set = (idCustomer, )
		
		
		_SQL = """select idProduct from cart where idCustomer = %s;  """
		cursor.execute(_SQL, (idCustomer_search_set))
		idProductDB = cursor.fetchall()

		idProductDBList = list()
		for id in idProductDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		products = dict()
		for id in idProductDBTuple:
			id_set = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, id_set)
			products[id] =  cursor.fetchall()
		
		#print(products)
		subTotal = 0
		for pro in products:
			subTotal = float(subTotal) + products[pro][0][2]
		
		if len(products) != 0:
			return render_template('my_cart.html', products=products, subTotal = subTotal)
		else:
			#flash('You\'re cart is empty')
			messages=['You\'re cart is empty']
		return render_template('my_cart.html',messages = messages, products=products)

@app.route('/customer_order' , methods=['GET', 'POST'])
@is_customer_logged_in
def customer_order() -> 'html':
	"""
	Manage orders of the customer.
	Insert the details of teh order to the database.
	Output: after inserting the products in the DB, return the home page of teh customer.
	"""
	subTotal = float(request.form['subTotal'])
	ipAddress = request.remote_addr
	#print(subTotal, ipAddress)

	with Usedatabase(app.config['dbconfig']) as cursor:
		idCustomer = session['customer_id']
		idCustomer_search_set = (idCustomer, )
				
		_SQL = """select idProduct from cart where idCustomer = %s;  """
		cursor.execute(_SQL, (idCustomer_search_set))
		idProductDB = cursor.fetchall()

		idProductDBList = list()
		for id in idProductDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			id_set = (id, )
			_SQL = """select cost from product where idProduct = %s ; """
			cursor.execute(_SQL, id_set)
			cost =  cursor.fetchone()[0]

			order_set = (idCustomer, id, 1, cost, ipAddress, )
			#print(order_set)

			_SQL = """insert into orders(idCustomer, idProduct, quantity, subTotal, remoteIPAddress) values(%s,%s,%s,%s,%s); """
			cursor.execute(_SQL, order_set)

			_SQL = """delete from cart where idProduct = %s ; """
			cursor.execute(_SQL, id_set)
	flash('Order Successfully placed')
	return redirect(url_for('customer_loggedin_home_page'))

@app.route('/my_orders')
@is_customer_logged_in
def my_orders() -> 'html':
	"""
	output the products from the user has ordered from database to the webpage
	output: all teh products that are ordered by the customer
	"""
	
	with Usedatabase(app.config['dbconfig']) as cursor:
		idCustomer = session['customer_id']
		idCustomer_search_set = (idCustomer, )
		
		
		_SQL = """select idProduct from orders where idCustomer = %s;  """
		cursor.execute(_SQL, (idCustomer_search_set))
		idProductDB = cursor.fetchall()

		idProductDBList = list()
		for id in idProductDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		products = dict()
		for id in idProductDBTuple:
			id_set = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, id_set)
			products[id] =  cursor.fetchall()
		
		#print(products)
		'''
		subTotal = 0
		for pro in products:
			subTotal = float(subTotal) + products[pro][0][2]
		'''
		if len(products) != 0:
			return render_template('my_orders.html', products=products)
		else:
			#flash('You\'re cart is empty')
			messages=['You don\'t have any orders']
		return render_template('my_orders.html',messages = messages, products=products)


@app.route('/delete_product_from_cart/<string:code>', methods=['GET', 'POST'])
@is_customer_logged_in
def delete_product_from_cart(code) -> 'html':
	"""
	Delete the product with the code from teh customer cart which is deleted.
	The is reflected in the DB and also on the my_cart webpage
	"""
	
	idCustomer = session['customer_id']
	#print(idCustomer)
	with Usedatabase(app.config['dbconfig']) as cursor:
		#code_set = (code, )
		_SQL = """delete from cart where idProduct = %s and idCustomer = %s;  """
		
		cursor.execute(_SQL, (code, idCustomer))
		flash("Item removed from cart")

	return redirect(url_for('my_cart'))

@app.route('/customer_view_product/<string:code>', methods=['GET', 'POST'])
@is_customer_logged_in
def customer_view_product(code) -> 'html':
	"""
	Display the individual product info.
	all the product details are displayed including the desctipiton and the category of the product .
	return: webpage with the product details.
	"""
	product = dict()
	with Usedatabase(app.config['dbconfig']) as cursor:
		code_set = (code, )
		_SQL = """select image, name, cost, description, categoryName, idProduct from product where idProduct = %s ; """
		
		cursor.execute(_SQL, code_set)
		product[int(code)] = cursor.fetchone()
		
	return render_template('customer_view_product.html',
		image=product[int(code)][0],
		name=product[int(code)][1],
		price=product[int(code)][2],
		desc = product[int(code)][3],
		category = product[int(code)][4],
		code=product[int(code)][5] )


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


"""
Below are all the methods that are related to the admin
"""
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login() -> 'html':
	"""
	Output: login page for the admin.
	Display the log-in form  for the admin of the website.
	"""
	
	#messages = []
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		userDetails = [username, password]

		for value in userDetails:
			if not value:
				flash('Please fill all the details')
				#messages = ['Please fill all the details']
				return render_template('admin_login.html')
		
		with Usedatabase(app.config['dbconfig']) as cursor:
				_SQL = """select username, password, email from admin; """
				cursor.execute(_SQL)
				loginDetailsDB = cursor.fetchall()

				for un in loginDetailsDB:					
					if username == un[0]:					
						#flash('Username or Email already taken')
						#if mysql41.verify(password, un[1]):
						if password == un[1]:						
							flash('Login successful')

							set_adminid_to_flask_app_config(un[0], un[2], password)

							return redirect(url_for('dashboard'))
			
			
		flash('Invalid username or password')
		#messages = ['Invalid username or password'] , messages=messages
	return render_template('admin_login.html')

@app.route('/admin_logout')
@is_admin_logged_in
def admin_logout() -> 'html':
	"""
	The admin logouts out of the website.
	Here the details of the admin from the session are cleared.
	Return: the login page of the admin.
	"""
	if 'admin_logged_in' in session:
		#session.clear()
		#session['admin_logged_in'] = False
		session.pop('admin_logged_in')
		session.pop('admin_id')
		session.pop('admin_username')
		session.pop('admin_email')
		session.pop('admin_password')
		flash('You are logged out')
		#messages = ['You are logged out']
		#return redirect(url_for('admin') )
	return redirect(url_for('admin_login'))

@app.route('/dashboard')
@is_admin_logged_in
def dashboard() -> 'html':
	"""
	Display the dashboard for the admin
	"""
	
	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """ select streetOrvillage, count(streetOrvillage) from customer group by streetOrvillage; """	
		cursor.execute(_SQL)
		street = cursor.fetchall()
		#print(data)
		_SQL = """ select cityOrTown, count(cityOrTown) from customer group by cityOrTown; """	
		cursor.execute(_SQL)
		city = cursor.fetchall()

		_SQL = """ select state, count(state) from customer group by state; """	
		cursor.execute(_SQL)
		state = cursor.fetchall()

		_SQL = """ select country, count(country) from customer group by country; """	
		cursor.execute(_SQL)
		country = cursor.fetchall()

		
		_SQL = """ select customer.username, count(cart.idProduct) from 
			customer, cart where customer.idCustomer=cart.idCustomer group by customer.username; """	
		cursor.execute(_SQL)
		d1 = cursor.fetchall()

		_SQL = """ select customer.username, count(orders.idProduct) from 
			customer, orders where customer.idCustomer=orders.idCustomer group by customer.username; """	
		cursor.execute(_SQL)
		d2 = cursor.fetchall()

	return render_template('admin.html', 
		street=street, 
		city=city, 
		state=state, 
		country=country, 
		productInCustomerCart=d1,
		orderedproducts=d2)

@app.route('/admin_view_product/<string:code>', methods=['GET', 'POST'])
@is_admin_logged_in
def admin_view_product(code) -> 'html':
	"""
	Display the individual product info.
	all the product details are displayed including teh desctipiton, category of the product and the quantity available.
	return: webpage with the product details.
	"""
	product = dict()
	with Usedatabase(app.config['dbconfig']) as cursor:
		code_set = (code, )
		_SQL = """select image, name, cost, description, categoryName, idProduct, quantityAvailable from product where idProduct = %s ; """
		
		cursor.execute(_SQL, code_set)
		product[int(code)] = cursor.fetchone()
		
	return render_template('admin_view_product.html',
		image=product[int(code)][0],
		name=product[int(code)][1],
		price=product[int(code)][2],
		desc = product[int(code)][3],
		category = product[int(code)][4],
		code=product[int(code)][5],
		quantity=product[int(code)][6] )

@app.route('/all_products')
@is_admin_logged_in
def all_products() -> 'html':
	"""
	Display all the products prsent in the database to the admin
	output: webpage containing all the products
	"""

	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """ select categoryName from category; """
		cursor.execute(_SQL)
		categoryNameDB = cursor.fetchall()

		categoryNameDBList = list()
		for name in categoryNameDB:
			categoryNameDBList.append(name[0])

		products = dict()
		for name in categoryNameDB:
			_SQL = """select image, name, cost, idProduct, quantityAvailable from product where categoryName = %s order by rand() ; """
			cursor.execute(_SQL, name)
			products[name] = cursor.fetchall()
	
	return render_template('admin_products.html', products = products)

@app.route('/frequent_products')
@is_admin_logged_in
def frequent_products() -> 'html':
	"""
	Display the frequently viewed products (those in the cart) by the customers to the admin 
	output: webpage containing freqeuntly viewed products
	"""

	frequently_viewed_products = dict()
	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """ select idProduct from cart group by idProduct order by rand() ; """
		cursor.execute(_SQL)
		productIdDB = cursor.fetchall()

		idProductDBList = list()
		for id in productIdDB:
			idProductDBList.append(id[0])

		idProductDBTuple = tuple(idProductDBList)

		for id in idProductDBTuple:
			idSet = (id, )
			_SQL = """select image, name, cost, idProduct from product where idProduct = %s ; """
			cursor.execute(_SQL, idSet)
			frequently_viewed_products[id] = cursor.fetchall()
	
	return render_template('admin_frequent_products.html', frequentProducts = frequently_viewed_products)

@app.route('/admin_customer_orders')
@is_admin_logged_in
def admin_customer_orders() -> 'html':
	"""
	Display all the ordered product details by the customers to the admin 
	output: webpage containing all the ordereded products detials
	"""

	with Usedatabase(app.config['dbconfig']) as cursor:
		#users = dict()
		#_SQL = """select image, name, cost, idProduct, quantityAvailable from product where categoryName = 'smartphone' order by rand() ; """
		_SQL = """select  
					idOrder, idCustomer, idProduct, quantity, orderTime, subTotal, remoteIPAddress, status
					from orders;
					"""
		cursor.execute(_SQL)
		
		orders = cursor.fetchall()
	
	
	return render_template('admin_customer_orders.html', orders = orders)

@app.route('/admin_category')
@is_admin_logged_in
def admin_category() -> 'html':
	"""
	Display the category of the products to the admin
	Also displays the number of products in the DB based on the cateory
	Return: webpage with category details
	"""
	with Usedatabase(app.config['dbconfig']) as cursor:
		_SQL = """select categoryName from category;"""
		cursor.execute(_SQL)
		
		category = cursor.fetchall()

		_SQL = """select categoryName, count(idProduct) from product group by categoryName;"""
		cursor.execute(_SQL)
		
		categoryNoOfProducts = cursor.fetchall()
	
	return render_template('admin_category.html', category = category, categoryNoOfProducts=categoryNoOfProducts)


@app.route('/all_users')
@is_admin_logged_in
def all_users() -> 'html':
	"""
	Display all the customer details to the admin
	Output: The customer details are displayed in the form of table on the webpage
	"""

	with Usedatabase(app.config['dbconfig']) as cursor:
		#users = dict()
		#_SQL = """select image, name, cost, idProduct, quantityAvailable from product where categoryName = 'smartphone' order by rand() ; """
		_SQL = """select  
					idCustomer, email, firstName, lastName, contact, houseNoOrFlatNo, streetOrvillage, cityOrTown, state, country, username
					from customer
					"""
		cursor.execute(_SQL)
		
		users = cursor.fetchall()

	
	return render_template('admin_all_users.html', users = users)

#run the app
if __name__ == '__main__':
	app.run(debug = True)
