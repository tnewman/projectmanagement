from abc import ABCMeta, abstractmethod
from configuration import ConfigurationFactory

class DatabaseFactory:
    @staticmethod
    def get_database():
        configuration = ConfigurationFactory.get_configuration()
        type = configuration.get_database_type()
        hostname = configuration.get_database_hostname()
        username = configuration.get_database_username()
        password = configuration.get_database_password()
        database_name = configuration.get_database_name()
        
        database_class = DatabaseFactory._get_database_class_from_str(type)
        
        return database_class(hostname, username, password, database_name)
    
    @staticmethod
    def _get_database_class_from_str(class_name):
        module_name = 'database'
        module = __import__(module_name)
        return getattr(module, class_name)

class Database:
    __metaclass__ = ABCMeta
    
    def __init__(self, hostname, username, password, database_name):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database_name = database_name
    
    def __enter__(self):
        self.open()
    
    def __exit__(self):
        self.close()
    
    @abstractmethod
    def open(self):
        return NotImplemented
    
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
        return NotImplemented
    
    def close(self):
        return NotImplemented
    
    def load_projects(self):
        sql = ('SELECT * FROM project;') 
        raise NotImplementedError
    
    def load_project(self, project_id):
        sql = ('SELECT * FROM project WHERE id = 0;')
        raise NotImplementedError
    
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