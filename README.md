# 1911_DBMS_LAB_PROJECT

# DBMS Lab project with Python(Flask) and MySql

# Technology Software Stack:
   1)VS Code
   2)MySql Workbench
   3)Dia Diagram
   4)Languages: Python, HTML, CSS, Jinja, SQL

# Requirements:
   1)Python
   2)Flask package
   	->sudo pip install flask 
   	(#command to install flask on linux system from the terminal.)
   3)MySql server 
   	(#follow standard porcedure found on the internet to install MySql server on your system.)

# Directory structure of the project:
 1911_DBMS_LAB_PROJECT
 1)app.py (#main file to rn the server for the project.)
 2)config.py (#configuration file containing the passwords and secret keys.)
 3)Database (#folder containing the sql scripts used when executing the commands on MySql server.)
    1)createTables.sql (#used MySql workbench and the terminal for the same.)
 4)dbcm.py 
 	  (#context manager file for datbase, connect to database, execute commands and close connection.)
 5)Diagrams 
 	  (#folder containing diagrams used in the project, Dia Diagram software was used to construct the diagrams.)
 6)README.md (#file containin the details of the project.)
 7)Screenshots (#file containing the screenshots of the project.)
 8)static (#folder with static file.)
 	  1)products(#folder containing the images used in the project.)
 	  2)website.css (#css file used for the project.)
 9)templates (#folder with the template html files of the project.)
   	1)admin_login.html
  	2)base.html
  	3)customer_login.html
  	4)my_account.html
  	5)signup.html
  	6)website.html
 10)WorkFlowDocumentation.txt (#time-wise work done documentation file.)

To run the app:
   ->open the project directory and run the app.py file with the below command
   ->python3 app.py (on the terminal)
   ->or directly run the server on the VS Code
