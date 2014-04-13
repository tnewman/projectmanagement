from abc import ABCMeta, abstractmethod
from configuration import ConfigurationFactory
from datainterchange import Complexity, Project, Task, Login
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
        self.database = None
    
    def __enter__(self):
        self.open()
    
    def __exit__(self):
        self.close()
    
    @abstractmethod
    def open(self):
        self.database = postgresql.open
    
    @abstractmethod
    def close(self):
        return NotImplemented
    
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

class PostgreSQL(Database):
    def open(self):
        self.database = psycopg2.connect(
            user = self.username,
            password = self.password,
            host = self.hostname,
            port = self.port,
            database = self.database_name
            )
    
    def close(self):
        self.database.close()
    
    def load_projects(self):
        projects = []
        sql = ('SELECT id, name, brief_description, description '
               'FROM project;') 
        
        cursor = self.database.cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        
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
               'FROM project WHERE id = ?;')
        
        cursor = self.database.cursor()
        cursor.execute(sql, project_id)
        
        row = cursor.fetchone()
        
        # Convert each Project row in the database to a Project object
        if row:
            project = Project()
            project.id = row[0]
            project.name = row[1]
            project.brief_description = row[2]
            project.description = row[3]
        else:
            return None
    
    def insert_project(self, project):
        sql = ('INSERT INTO project (name, brief_description, '
               'description) VALUES (?, ?, ?);')
        raise NotImplementedError
    
    def update_project(self, project):
        sql = ('UPDATE project SET name=?, brief_description=?, '
               'description=? WHERE id=?;')
        raise NotImplementedError
        
    def delete_project(self, project_id):
        sql = ('DELETE FROM project WHERE id=?;')
        raise NotImplementedError
    
    def load_tasks(self, project_id):
        sql = ('SELECT id, project_id, name, brief_description, '
               'description, complexity, due_date, status FROM task '
               'WHERE project_id=?;')
        raise NotImplementedError
    
    def load_task(self, project_id, task_id):
        sql = ('SELECT id, project_id, name, brief_description, '
               'description, complexity, due_date, status FROM task '
               'WHERE id=? AND project_id=?;')
        raise NotImplementedError
    
    def insert_task(self, task):
        sql = ('INSERT INTO task (project_id, name, brief_description, '
               'description, complexity, due_date, status) VALUES '
               '(?, ?, ?, ?, ?, ?, ?);')
        raise NotImplementedError
        
    def update_task(self, task):
        sql = ('UPDATE task SET project_id=?, name=?, '
               'brief_description=?, description=?, complexity=?, '
               'due_date=?, status=? WHERE id=? AND project_id=?;')
        raise NotImplementedError
        
    def delete_task(self, task_id, project_id):
        sql = ('DELETE FROM task WHERE id=? AND project_id=?;')
        raise NotImplementedError
    
    def load_login(self, username):
        sql = ('SELECT username, password FROM login WHERE username=?;')
        raise NotImplementedError