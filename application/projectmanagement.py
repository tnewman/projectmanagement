from flask import Flask
app = Flask(__name__)

@app.route('/projects')
def view_projects():
    return 'Test viewing all the projects'

@app.route('/projects/add')
def add_project():
    return 'Test adding of the project'    

@app.route('/project/<int:project_id>')
def view_project(project_id):
    return 'Test viewing of the project'

@app.route('/project/update/<int:project_id>')
def update_project(project_id):
    return 'Test updating of the project'

@app.route('/project/delete/<int:project_id>')
def delete_project(project_id):
    return 'Test deleting of the project'

@app.route('/tasks')
def view_tasks():
    return 'Test viewing of all tasks'

@app.route('/tasks/add')
def add_task():
    return 'Test adding of the task'

@app.route('/task/<int:task_id>')
def view_task(task_id):
    return 'Test viewing of the task'

@app.route('/task/<int:task_id>/update')
def update_task(task_id):
    return 'Test updating of the task'

@app.route('/task/<int:task_id>/delete')
def delete_task(task_id):
    return 'Test deleting of the task'

if __name__ == '__main__':
    app.run()