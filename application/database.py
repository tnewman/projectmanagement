from abc import ABCMeta, abstractmethod
from configuration import ConfigurationFactory
from models import Complexity, Status, Project, Task, Login
import psycopg2

class DatabaseFactory:
    @staticmethod
    def get_database():
        configuration = ConfigurationFactory.get_configuration()
        type = configuration.get_database_type()
        hostname = configuration.get_database_hostname()
        port = configuration.get_database_port()
        username = configuration.get_database_username()
        password = configuration.get_database_password()
        database_name = configuration.get_database_name()
        
        database_class = DatabaseFactory._get_database_class_from_str(type)
        
        return database_class(hostname, port, username, password, database_name)
    
    @staticmethod
    def _get_database_class_from_str(class_name):
        module_name = 'database'
        module = __import__(module_name)
        return getattr(module, class_name)

class Database:
    __metaclass__ = ABCMeta
    
    def __init__(self, hostname, port, username, password, database_name):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.connection = None
    
    @abstractmethod
    def load_projects(self):
        return NotImplemented
    
    @abstractmethod
    def load_project(self, project_id):
        return NotImplemented
    
    @abstractmethod
    def insert_project(self, project):
        return NotImplemented
    
    @abstractmethod
    def update_project(self, project):
        return NotImplemented
    
    @abstractmethod
    def delete_project(self, project_id):
        return NotImplemented
    
    @abstractmethod
    def load_tasks(self, project_id):
        return NotImplemented
    
    @abstractmethod
    def load_task(self, project_id, task_id):
        return NotImplemented
    
    @abstractmethod
    def insert_task(self, task):
        return NotImplemented
    
    @abstractmethod
    def update_task(self, task):
        return NotImplemented
    
    @abstractmethod
    def delete_task(self, task_id):
        return NotImplemented
    
    @abstractmethod
    def load_user(self, username):
        return NotImplemented

class DataCalculationError(Exception):
    def __str__(self):
        print('DataCalculationError: Error related to calculation.')

class DataIntegrityError(Exception):
    def __str__(self):
        print('DataIntegrityError: Error related to constraint violation.')

class PostgreSQL(Database):    
    def load_projects(self):
        projects = []
        sql = ('SELECT id, name, brief_description, description '
               'FROM project;')
        parameters = []
        
        rows = self._execute_query(sql, parameters)
        
        # Convert each Project row in the database to a Project object
        for row in rows:
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.brief_description = row[2]
            project.description = row[3]
            
            projects.append(project)
        
        return projects
    
    def load_project(self, project_id):
        sql = ('SELECT id, name, brief_description, description '
               'FROM project WHERE id = %s;')
        parameters = [project_id]
        
        rows = self._execute_query(sql, parameters)
        
        # Convert the Project row in the database to a Project object
        if rows:
            row = rows[0]
            
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.brief_description = row[2]
            project.description = row[3]
            
            return project
        else:
            return None
    
    def insert_project(self, project):
        sql = ('INSERT INTO project (name, brief_description, '
               'description) VALUES (%s, %s, %s);')
        parameters = [project.name, project.brief_description, 
                      project.description]
        
        self._execute_non_query(sql, parameters)
    
    def update_project(self, project):
        sql = ('UPDATE project SET name=%s, brief_description=%s, '
               'description=%s WHERE id=%s;')
        parameters = [project.name, project.brief_description, 
                      project.description, project.id]
        
        self._execute_non_query(sql, parameters)
    
    def delete_project(self, project_id):
        sql = ('DELETE FROM project WHERE id=%s;')
        parameters = [project_id]
        
        cursor = self.database.cursor()
        cursor.execute(sql, parameters)
        self.database.commit()
    
    def load_tasks(self, project_id):
        tasks = []
        sql = ('SELECT id, project_id, name, brief_description, '
               'description, complexity, due_date, status FROM task '
               'WHERE project_id=%s;')
        parameters = [project_id]
        
        rows = self._execute_query(sql, parameters)
        
        # Convert each Task row in the database to a Task object
        for row in rows:
            task = Task()
            task.id = row[0]
            task.project_id = row[1]
            task.name = row[2]
            task.brief_description = row[3]
            task.description = row[4]
            
            try:
                task.complexity = Complexity(row[5])
            except(ValueError):
                task.complexity = Complexity.UNKNOWN
            
            task.due_date = row[6]
            
            tasks.append(task)
        
        return tasks
    
    def load_task(self, project_id, task_id):
        sql = ('SELECT id, project_id, name, brief_description, '
               'description, complexity, due_date, status FROM task '
               'WHERE project_id=%s AND id=%s;')
        parameters = [project_id, task_id]
        
        rows = self._execute_query(sql, parameters)
        
        if rows:
            row = rows[0]
        
            task = Task()
            task.id = row[0]
            task.project_id = row[1]
            task.name = row[2]
            task.brief_description = row[3]
            task.description = row[4]
            
            try:
                task.complexity = Complexity(row[5])
            except(ValueError):
                task.complexity = Complexity.UNKNOWN
            
            task.due_date = row[6]
            
            return task
        else:
            return None
    
    def insert_task(self, task):
        sql = ('INSERT INTO task (project_id, name, brief_description, '
               'description, complexity, due_date, status) VALUES '
               '(%s, %s, %s, %s, %s, %s, %s);')
        parameters = [task.project_id, task.name, task.brief_description, 
                      task.description, str(task.complexity), task.due_date, 
                      str(task.status)]
        
        self._execute_non_query(sql, parameters)
        
    def update_task(self, task):
        sql = ('UPDATE task SET project_id=%s, name=%s, '
               'brief_description=%s, description=%s, complexity=%s, '
               'due_date=%s, status=%s WHERE id=%s AND project_id=%s;')
        parameters = [task.project_id, task.name, task.brief_description, 
                      task.description, str(task.complexity), task.due_date, 
                      str(task.status), task.id, task.project_id]
        
        self._execute_non_query(sql, parameters)
        
    def delete_task(self, project_id, task_id):
        sql = ('DELETE FROM task WHERE id=%s AND project_id=%s;')
        parameters = [task_id, project_id]
        
        self._execute_non_query(sql, parameters)
    
    def load_login(self, username):
        sql = ('SELECT id, username, password FROM login WHERE username=%s;')
        parameters = [username]
        
        self._execute_query(sql, parameters)
        
        # Convert the Login row in the database to a Login object
        if rows:
            row = rows[0]
            login = Login()
            login.id = row[0]
            login.username = row[1]
            login.password = row[2]
            
            return login
        else:
            return None
    
    def _open(self):
        self.connection = psycopg2.connect(
            user = self.username,
            password = self.password,
            host = self.hostname,
            port = self.port,
            database = self.database_name
            )
    
    def _close(self):
        self.connection.close()
    
    def _execute_query(self, sql, parameters):
        self._open()
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, parameters)
            rows = cursor.fetchall()
        except(psycopg2.IntegrityError):
            raise(DataIntegrityError)
        except(psycopg2.DataError):
            raise(DataCalculationError)
        
        self._close()
        
        return rows
    
    def _execute_non_query(self, sql, parameters):
        self._open()
        
        try:
            cursor = self.connection.cursor()
            rows = cursor.execute(sql, parameters)
            self._connection.commit()
        except(psycopg2.IntegrityError):
            raise(DataIntegrityError)
        except(psycopg2.DataError):
            raise(DataCalculationError)
        
        self._close()

