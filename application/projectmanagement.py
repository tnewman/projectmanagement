from database import DatabaseFactory
from flask import Flask, g, render_template, redirect, session, url_for
app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
    if not check_session_login():
        return redirect(url_for('login'))
    
    return redirect(url_for('projects'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if check_session_login():
        return redirect(url_for('logout'))
    
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    response.delete_cookie(app.session_cookie_name)

@app.route('/projects', methods=['GET'])
def projects():
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('viewprojects.html')

@app.route('/projects/addproject', methods=['POST'])
def add_project():
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('addproject.html')

@app.route('/project/<int:project_id>')
def project(project_id, methods=['GET']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('viewproject.html')

@app.route('/project/<int:project_id>/modifyproject')
def modify_project(project_id, methods=['GET', 'POST']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('modifyproject.html')

@app.route('/project/<int:project_id>/deleteproject')
def delete_project(project_id, methods=['POST']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return 'Test deleting of the project'

@app.route('/project/<int:project_id>/addtask')
def add_task(project_id, methods=['GET', 'POST']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('addproject.html')

@app.route('/project/<int:project_id>/task/<int:task_id>')
def task(project_id, task_id, methods=['GET']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('viewtask.html')

@app.route('/project/<int:project_id>/task/<int:task_id>/modifytask')
def modify_task(project_id, task_id, methods=['GET', 'POST']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return render_template('modifytask.html')

@app.route('/project/<int:project_id>/task/<int:task_id>/deletetask')
def delete_task(project_id, task_id, methods=['POST']):
    if not check_session_login():
        return redirect(url_for('login'))
    
    return 'Test deleting of the task'

def check_session_login():
    g.database = DatabaseFactory.get_database()
    
    if 'username' in session:
        g.user = g.database.load_login(session['username'])
        
        if g.user:
            return True
    
    return False

if __name__ == '__main__':
    app.run()