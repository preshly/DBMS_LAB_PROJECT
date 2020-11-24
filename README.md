
1911 DBMS LAB PROJECT

DBMS Lab project with Python(Flask) and MySql

Technology Software Stack:
	1)VS Code
	2)MySql Workbench
	3)Dia Diagram
	4)Languages: Python, HTML, CSS, Jinga, SQL

Requirements:
	1)Python
	2)Flask package
		->sudo pip install flask 
		(#command to install flask on linux system from the terminal.)
	3)MySql server 
		(#follow standard porcedure found on the internet to install MySql server on your system.)


Directory structure of the project:
1911_DBMS_LAB_PROJECT
├── app.py (#main file to rn the server for the project.)
├── config.py (#configuration file containing the passwords and secret keys.)
├── Database (#folder containing the sql scripts used when executing the commands on MySql server.)
│   └── createTables.sql (#used MySql workbench and the terminal for the same.)
├── dbcm.py 
|	(#context manager file for datbase, connect to database, execute commands and close connection.)
├── Diagrams 
|	(#folder containing diagrams used in the project, Dia Diagram software was used to construct the 
|		diagrams.)
├── __pycache__
│   ├── config.cpython-37.pyc
│   └── dbcm.cpython-37.pyc
├── README.md (#file containin the details of the project.)
├── Screenshots (#file containing the screenshots of the project.)
├── static (#folder with static file.)
│   ├── products(#folder containing the images used in the project.)
│   └── website.css (#css file used for the project.)
├── templates (#folder with the template html files of the project.)
│   ├── admin_login.html
│   ├── base.html
│   ├── customer_login.html
│   ├── my_account.html
│   ├── signup.html
│   └── website.html
└── WorkFlowDocumentation.txt (#time-wise work done documentation file.)

To run the app:
->open the project directory and run the app.py file with the below command
->python3 app.py (on the terminal)
->or directly run the server on the VS Code