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
* VirtualEnv (not required in development but recommended)

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
  - `pip install -r requirements.txt
* Create a file called `.env`.
  - Add the following variables to the `.env`:
```bash
DATABASE_URL=scheme://dbusername:dbpassword@dbhost:dbport/dbname
DEBUG=False/True (toggles debug mode)
SECRET_KEY=A long, random, key used for cookie encryption. When this changes, all cookies expire.
```
* Initialize the database schema with tables and the initial login:
  - 
