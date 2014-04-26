from datetime import datetime
from flask import *
from .model import *
from . import database
import jinja2
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['DATABASE_URL'] = os.environ['DATABASE_URL']

app.debug = bool(os.environ['DEBUG'])

@app.route('/')
def index():
    if not 'user_id' in session:
        return redirect(url_for('login_get'))
    
    return redirect(url_for('projects'))

@app.route('/login', methods=['GET'])
def login_get():
    if 'user_id' in session:
        return redirect(url_for('projects'))
    
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
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
    session.clear()
    
    return redirect(url_for('login_get'))

@app.route('/projects', methods=['GET'])
def projects():
    if not 'user_id' in session:
        return redirect(url_for('logout'))
    
    db = get_database()
    
    request.projects = db.load_projects()
    
    return render_template('viewprojects.html')

@app.route('/projects/addproject', methods=['GET', 'POST'])
def add_project():
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

@app.route('/project/<int:project_id>/deleteproject')
def delete_project(project_id, methods=['POST']):
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
    name_field = request.form.get('name')
    brief_description_field = request.form.get('briefdescription')
    description_field = request.form.get('description')
    
    errors = []
    
    if name_field == '':
        errors.append('name_blank')
    else:
        try:
            project.name = name_field
        except(ValueError):
            errors.append('name_invalid')
    
    if brief_description_field == '':
        errors.append('brief_description_blank')
    else:
        try:
            project.brief_description = brief_description_field
        except(ValueError):
            errors.append('brief_description_invalid')
    
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
        if current_project.name == task.name:
            # The name can obviously be the same if the same task is 
            # being updated
            if current_project.id != project.id:
                errors.append('name_duplicate')
                break
    
    return errors

@app.route('/project/<int:project_id>/task/<int:task_id>', methods=['GET'])
def task(project_id, task_id):
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
    name_field = request.form.get('name')
    brief_description_field = request.form.get('briefdescription')
    description_field = request.form.get('description')
    complexity_field = request.form.get('complexity')
    due_date_field = request.form.get('duedate')
    status_field = request.form.get('status')
    
    errors = []
    
    if name_field == '':
        errors.append('name_blank')
    else:
        try:
            task.name = name_field
        except(ValueError):
            errors.append('name_invalid')
    
    if brief_description_field == '':
        errors.append('brief_description_blank')
    else:
        try:
            task.brief_description = brief_description_field
        except(ValueError):
            errors.append('brief_description_invalid')
    
    if description_field == '':
        errors.append('description_blank')
    else:
        try:
            task.description = description_field
        except(ValueError):
            errors.append('description_invalid')
    
    if complexity_field == '':
        errors.append('complexity_blank')
    else:
        try:
            task.complexity = complexity_field
        except(ValueError):
            errors.append('complexity_invalid')
    
    if due_date_field == '':
        errors.append('due_date_blank')
    else:
        try:
            task.due_date = due_date_field
        except(ValueError):
            errors.append('due_date_invalid')
    
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
    return render_template('404.html'), 404
    
@app.errorhandler(500)
def internal_server_error(error):
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
    with app.app_context():
        db = get_database()
        db.initialize_database(username, password)