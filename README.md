Project Management
=================
Project Management offers a basic Project Management Application 
where users can create projects. Each project has a list of tasks 
with a due date, complexity, and completion status. The application 
displays whether or not a task is past its due date. Project Management 
is designed for Heroku; however, porting it to any UNIX environment 
would be trivial.

Requirements
------------
* Heroku Toolbelt
* Python 3.4+
* PIP
* PostgreSQL (the application is designed to support multiple databases, 
  but they have not been implemented yet)
* VirtualEnv

Local Development Setup
-----------------------
This setup should only be used for testing purposes on a local machine. 
The built-in Flask web server is not designed to support production 
requirements for concurrency; however, the built-in web server has the 
benefit of reloading changes automatically and Windows support (both of 
which are lacking in Gunicorn).

* Install the required components
* Clone this repository
* Navigate into the repository folder via the command line
* Create the VirtualEnv: `virtualenv venv`
* Activate the VirtualEnv shell:
  - UNIX: `source bin/activate`
  - Windows: `venv\Scripts\activate`
* Install the required packages from requirements.txt with pip:
  - `pip install -r requirements.txt`
* Create a file called `configuration.cfg`.
  - Add the following variables to `configuration.cfg`:
```
[Configuration]
DATABASE_URL=scheme://dbusername:dbpassword@dbhost:dbport/dbname
DEBUG=False/True (toggles debug mode)
SECRET_KEY=A long, random, key used for cookie encryption. When this changes, all cookies expire.
```
* Initialize the database schema with tables and the initial login:
  - DO NOT complete these steps if the database is already set up.
  - `python projectmanagement.py -initializedatabase USERNAME PASSWORD`
  - `USERNAME` and `PASSWORD` are the initial login credentials that 
    will be used to access the application.

Running Local Development Server
--------------------------------
* Navigate into the repository folder via the command line
* Activate the VirtualEnv shell:
  - UNIX: `source bin/activate`
  - Windows: `venv\Scripts\activate`
* Run the server: `python projectmanagement.py`
* The application can be accessed at: `http://localhost:5000`

Heroku Setup
------------
* Clone this repository
* Navigate into the repository folder via the command line
* Log into your Heroku account: `heroku login`
* Create a new Heroku application: `heroku create`
* Provision a PostgreSQL Development Database: `heroku addons:add heroku-postgresql:dev`
* Set the debug mode environmental variable to false: `heroku config:set DEBUG=False`
* Set the secret key environmental variable (make sure you change this 
  to a unique value): `heroku config:set SECRET_KEY=YOURKEYHERE`
* Push the application to Heroku: `git push heroku master`
* Disable all of the Web Dynos: `heroku ps:scale web=0`
* Enter the Heroku BASH prompt: `heroku run bash`
* Create the database schema: `python projectmanagement.py -initializedatabase USERNAME PASSWORD`
  - `USERNAME` and `PASSWORD` are the username and password that will be 
    used to log into the application initially
* Run a Web Dyno: `heroku ps:scale web=1`

Heroku Redeployment
-------------------
* After making changes to the application, the application can be pushed 
  to Heroku: `git push heroku master`
* Any changes to the database schema will require the database to be 
  altered.