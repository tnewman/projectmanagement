# File: projectmanagement.py
# Description: Provides the Project Management application routing and 
#              business logic.
# Date: 2014/04/27
# Programmer: Thomas Newman

''' projectmanagement provides the Project Management application routing and 
    business logic. '''

from datetime import datetime
from flask import *
from .model import *
from . import database
import jinja2
import os

# Set the Flask application that will be served to this application
app = Flask(__name__)

# Set the secret key for cookie encryption to the secret key stored in 
# the environmental variables.
app.secret_key = os.environ.get('SECRET_KEY')

# Set the application database URL to the database URL stored in the 
# environmental variables.
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')

# Set the debug mode for the application to the debug mode stored in the 
# environmental variables.
app.debug = bool(os.environ.get('DEBUG'))

@app.route('/')
def index():
    ''' Handles the get request for the index.
    
        Displays the login form if the user is not logged in.

        Redirects to the project list if the user is already logged 
        in. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('login_get'))
    
    return redirect(url_for('projects'))

@app.route('/login', methods=['GET'])
def login_get():
    ''' Handles the get request to login in.
        
        Returns:
            Displays the login form if the user is not logged in.

            Redirects to the project list if the user is already logged 
            in. '''
    
    # If the user is not logged in, redirect to the login form
    if 'user_id' in session:
        return redirect(url_for('projects'))
    
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    ''' Handles the post request to login in.
        
        Post Data:
            username (str) - The username to use for login.
            password (str) - The password to use for login.
            
        Returns:
            Redirects to the login form if the login fails (input errors 
            or the user does not exist in the database).
            
            Redirects to the project list if login is successful. '''
    
    request.errors = []
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == '':
        request.errors.append('username_blank')
    
    if password == '':
        request.errors.append('password_blank')
    
    # If the basic field validation passes, check against the database
    if not request.errors:
        db = get_database()
        login = db.load_login(username)
        
        # A record was found for the username in the database
        if login != None:
            # The username and password are correct
            if login.check_login(username, password):
                session['user_id'] = login.id
                return redirect(url_for('projects'))
            else:
                request.errors.append('password_incorrect')
        else:
            request.errors.append('username_not_exist')
    
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    ''' Handles the get request to log out the user.
        
        Returns:
            Displays the login form. '''
    
    # Log the user out and redirect to the login form
    session.clear()
    
    return redirect(url_for('login_get'))

@app.route('/projects', methods=['GET'])
def projects():
    ''' Handles the get request to display a list of all projects.
        
        Returns:
            Displays a list of all projects. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.projects = db.load_projects()
    
    return render_template('viewprojects.html')

@app.route('/projects/addproject', methods=['GET', 'POST'])
def add_project():
    ''' Handles the post request to add a project.
    
        Handles the get request to display the add project form.
        
        Post Data:
            name (str) - The name of the project.
            briefdescription (str) - A brief description of the project.
            description (str) - A description of the project.
            
        Returns:
            Redirects to the project list if the project is added successfully.
            
            Displays the modify project form if the post data contains errors. '''

    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    request.project = Project()
    
    if request.method == 'POST':
        request.errors = _validate_project_post(request.project)
        
        db = get_database()
        
        if not request.errors:
            db.insert_project(request.project)
            return redirect(url_for('projects'))
    
    return render_template('addproject.html')

@app.route('/project/<int:project_id>', methods=['GET'])
def project(project_id):
    ''' Handles the get request to display a project.
        
        URL Args:
            project_id (int): The id of the project to display.
            
        Returns:
            Displays the requested project if the project exists.
            
            Triggers a 404 Not Found Error if the project does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.project = db.load_project(project_id)
    request.tasks = db.load_tasks(project_id)
    
    if not request.project:
        abort(404)
    
    return render_template('viewproject.html')

@app.route('/project/<int:project_id>/modifyproject', methods=['GET', 'POST'])
def modify_project(project_id):
    ''' Handles the post request to modify a project.
    
        Handles the get request to display the modify project form.
        
        URL Args:
            project_id (int): The id of the project to modify.
        
        Post Data:
            name (str) - The name of the project.
            briefdescription (str) - A brief description of the project.
            description (str) - A description of the project.
            
        Returns:
            Redirects to the modified project if modification is successful.
            
            Displays the modify project form if the post data contains errors.
            
            Triggers a 404 Not Found Error if the project requested for 
            modification does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.project = db.load_project(project_id)
    
    # Cannot modify a project that does not exist
    if not request.project:
        abort(404)
    
    if request.method == 'POST':
        request.errors = _validate_project_post(request.project)
        
        if not request.errors:
            db.update_task(request.project)
            return redirect(url_for('project', project_id=project_id))
    
    return render_template('modifyproject.html')

@app.route('/project/<int:project_id>/deleteproject', methods=['POST'])
def delete_project(project_id):
    ''' Handles the post request to delete a project.
        
        URL Args:
            project_id (int): The id of the project to delete.
            
        Returns:
            Redirects to the project list if deletion is successful.
            
            Triggers a 404 Not Found Error if the project requested for 
            deletion does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    project = db.load_project(project_id)
    
    # Cannot delete a task for a project that does not exist
    if not project:
        abort(404)
    
    db.delete_project(project_id)
    
    return redirect(url_for('projects'))

def _validate_project_post(project):
    ''' Validates the project data from the post request.
        
        Args:
            project (Project): The project to store the project information 
                               parsed from the post to.
            
        Returns:
            ([str]): A list of strings describing the errors that were 
                     encountered during validation. '''
    
    name_field = request.form.get('name')
    brief_description_field = request.form.get('briefdescription')
    description_field = request.form.get('description')
    
    errors = []
    
    # Validate the name field
    if name_field == '':
        errors.append('name_blank')
    else:
        try:
            project.name = name_field
        except(ValueError):
            errors.append('name_invalid')
    
    # Validate the brief description field
    if brief_description_field == '':
        errors.append('brief_description_blank')
    else:
        try:
            project.brief_description = brief_description_field
        except(ValueError):
            errors.append('brief_description_invalid')
    
    # Validate the description field
    if description_field == '':
        errors.append('description_blank')
    else:
        try:
            project.description = description_field
        except(ValueError):
            errors.append('description_invalid')
    
    # Make sure the name is not a duplicate
    db = get_database()
    projects = db.load_projects()
    
    for current_project in projects:
        if current_project.name == project.name:
            # The name can obviously be the same if the same task is 
            # being updated
            if current_project.id != project.id:
                errors.append('name_duplicate')
                break
    
    return errors

@app.route('/project/<int:project_id>/task/<int:task_id>', methods=['GET'])
def task(project_id, task_id):
    ''' Handles the get request to display a task.
        
        URL Args:
            project_id (int): The id of the project containing the task 
                              to display.
            
            task_id (int): The id of the task to display.
            
        Returns:
            Displays the requested task if the task exists.
            
            Triggers a 404 Not Found Error if the task does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.project = db.load_project(project_id)
    request.task = db.load_task(project_id, task_id)
    
    if not request.project or not request.task:
        abort(404)
    
    return render_template('viewtask.html')

@app.route('/project/<int:project_id>/addtask', methods=['GET', 'POST'])
def add_task(project_id):
    ''' Handles the post request to add a project task.
    
        Handles the get request to display the add task form.
        
        URL Args:
            project_id (int): The id of the project to add a task to.
        
        Post Data:
            name (str) - The name of the task.
            briefdescription (str) - A brief description of the task.
            description (str) - A description of the task.
            complexity (Complexity str) - The complexity of the task.
            duedate (YYYY-MM-DD str) - The due date of the task.
            status (Status str) - The completion status of the task.
            
        Returns:
            Redirects to the project containing the task if modification 
            is successful.
            
            Displays the modify task form if the post data contains errors.
            
            Triggers a 404 Not Found Error if the project that a task 
            will be added to does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.project = db.load_project(project_id)
    
    # Cannot add a task for a project that does not exist
    if not project:
        abort(404)
    
    request.task = Task()
    request.task.project_id = project_id
    
    if request.method == 'POST':
        request.errors = _validate_task_post(request.task)
        
        if not request.errors:
            db.insert_task(request.task)
            return redirect(url_for('project', project_id=project_id))
    
    return render_template('addtask.html')

@app.route('/project/<int:project_id>/task/<int:task_id>/modifytask', methods=['GET', 'POST'])
def modify_task(project_id, task_id):
    ''' Handles the post request to modify a project task.
    
        Handles the get request to display the modify task form.
        
        URL Args:
            project_id (int): The id of the project containing the task to 
                              modify.
            
            task_id (int): The id of the task to modify.
        
        Post Data:
            name (str) - The name of the task.
            briefdescription (str) - A brief description of the task.
            description (str) - A description of the task.
            complexity (Complexity str) - The complexity of the task.
            duedate (YYYY-MM-DD str) - The due date of the task.
            status (Status str) - The completion status of the task.
            
        Returns:
            Redirects to the modified task if modification is successful.
            
            Displays the modify task form if the post data contains errors.
            
            Triggers a 404 Not Found Error if the task requested for 
            modification does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.project = db.load_project(project_id)
    
    # Cannot add a task for a project that does not exist
    if not project:
        abort(404)
    
    request.task = db.load_task(project_id, task_id)
    
    # Cannot modify a task that does not exist
    if not request.task:
        abort(404)
    
    if request.method == 'POST':
        request.errors = _validate_task_post(request.task)
        
        if not request.errors:
            db.update_task(request.task)
            return redirect(url_for('task', project_id=project_id, 
                                task_id=task_id))
    
    return render_template('modifytask.html')

@app.route('/project/<int:project_id>/task/<int:task_id>/deletetask', methods=['POST'])
def delete_task(project_id, task_id):
    ''' Handles the post request to delete a task from a project.
        
        URL Args:
            project_id (int): The id of the project containing the task to 
                              be removed.
            
            task_id (int): The id of the task to remove.
            
        Returns:
            Redirects to the project containing the task if deletion is 
            successful.
            
            Triggers a 404 Not Found Error if the task requested for 
            deletion does not exist. '''
    
    # If the user is not logged in, redirect to the login form
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    project = db.load_project(project_id)
    
    # Cannot delete a task for a project that does not exist
    if not project:
        abort(404)
    
    request.task = db.load_task(project_id, task_id)
    
    # Cannot delete a project that does not exist
    if not request.task:
        abort(404)
    
    db.delete_task(project_id, task_id)
    
    return redirect(url_for('project', project_id=project_id))

def _validate_task_post(task):
    ''' Validates the task data from the post request.
        
        Args:
            task (Task): The task to store the task information 
                         parsed from the post to.
            
        Returns:
            ([str]): A list of strings describing the errors that were 
                     encountered during validation '''
    
    name_field = request.form.get('name')
    brief_description_field = request.form.get('briefdescription')
    description_field = request.form.get('description')
    complexity_field = request.form.get('complexity')
    due_date_field = request.form.get('duedate')
    status_field = request.form.get('status')
    
    errors = []
    
    # Validate the name field
    if name_field == '':
        errors.append('name_blank')
    elif len(name_field) > 50:
        errors.append('name_length')
    else:
        try:
            task.name = name_field
        except(ValueError):
            errors.append('name_invalid')
    
    # Validate the brief description field
    if brief_description_field == '':
        errors.append('brief_description_blank')
    elif len(brief_description_field) > 50:
        errors.append('brief_description_length')
    else:
        try:
            task.brief_description = brief_description_field
        except(ValueError):
            errors.append('brief_description_invalid')
    
    # Validate the description field
    if description_field == '':
        errors.append('description_blank')
    elif len(description_field) > 1000:
        errors.append('description_length')
    else:
        try:
            task.description = description_field
        except(ValueError):
            errors.append('description_invalid')
    
    # Validate the complexity field
    if complexity_field == '':
        errors.append('complexity_blank')
    else:
        try:
            task.complexity = complexity_field
        except(ValueError):
            errors.append('complexity_invalid')
    
    # Validate the due date field
    if due_date_field == '':
        errors.append('due_date_blank')
    else:
        try:
            task.due_date = due_date_field
        except(ValueError):
            errors.append('due_date_invalid')
    
    # Validate the status field
    if status_field == '':
        errors.append('status_blank')
    else:
        try:
            task.status = status_field
        except(ValueError):
            errors.append('status_invalid')
    
    # Make sure the name is not a duplicate
    db = get_database()
    tasks = db.load_tasks(task.project_id)
    
    for current_task in tasks:
        if current_task.name == task.name:
            # The name can obviously be the same if the same task is 
            # being updated
            if current_task.id != task.id:
                errors.append('name_duplicate')
                break
    
    return errors

@app.errorhandler(404)
def not_found(error):
    ''' Renders the page for 404 Not Found and sets the status code to 
        404. '''
    
    return render_template('404.html'), 404

@app.errorhandler(405)
def not_found(error):
    ''' Renders the page for 405 Method Not Supported and sets the 
        status code to 405. '''
    
    return render_template('405.html'), 405
    
@app.errorhandler(500)
def internal_server_error(error):
    ''' Renders the page for 500 Internal Server Error and sets the 
        status code to 500. '''
    
    return render_template('500.html'), 500

def get_database():
    ''' Returns the request's database object. The database object is 
        created if it does not exist yet. '''
    
    if not hasattr(g, 'database'):
        database_url = app.config['DATABASE_URL']
        g.database = database.get_database_from_url(database_url)
        g.database.open()
    
    return g.database

@app.teardown_appcontext
def close_database(error):
    ''' Closes the request's database object at the end of the request 
        if one was created. '''
    
    if hasattr(g, 'db'):
        g.database.close()

def initialize_database(username, password):
    ''' Initializes the database and create a user account with the 
        supplied username and password.
        
        Args:
            username (str): The username of the user to create.
            
            password (str): The password of the user to create. '''
    
    with app.app_context():
        db = get_database()
        db.initialize_database(username, password)