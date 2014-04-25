''' database contains classes to provide interaction with 
    a persistent data store.'''

from abc import ABCMeta, abstractmethod
from model import Complexity, Status, Project, Task, Login
import urllib.parse
import psycopg2

def get_database_from_url(database_url_str):
    ''' Uses a database URL to return an instance of the class that can 
        be found in the database module.
        
        Args:
            class_name(str): The name of the class to convert. The name 
            must exist in the database module.
        
        Returns:
            A class object derived from :class:`Database`
        
        Raises:
            AttributeError: The specified class does not exist.'''
    
    database_url = urllib.parse.urlparse(database_url_str)
    
    engine = database_url.scheme
    database = database_url.path[1:]
    username = database_url.username
    password = database_url.password
    host = database_url.hostname
    port = database_url.port
    
    if engine == 'postgres':
        db_class = PostgreSQL
    else:
        raise Exception('Invalid database engine specified.')
    
    return db_class(host, port, username, password, database)

class Database:
    ''' Abstract base class specifying the interfaces that all database 
        classes are to provide to allow consistent data access, regardless 
        of the underlying data store.
        
        This class should never be used directly because none of the 
        methods are implemented.'''
    
    __metaclass__ = ABCMeta
    
    def __init__(self, hostname, port, username, password, database_name):
        ''' Constructor '''
        
        #: (str): The database's hostname.
        self.hostname = hostname
        
        #: (int): The database's port number.
        self.port = port
        
        #: (str): The username to access the database.
        self.username = username
        
        #: (str): The password to access the database.
        self.password = password
        
        #: (str): The name of the database.
        self.database_name = database_name
        
        #: (Connection): The database connection object.
        self._connection = None
    
    def open(self):
        ''' Opens the database connection.'''
        
        return NotImplemented
    
    def close(self):
        ''' Closes the database connection.'''
        
        return NotImplemented
    
    @abstractmethod
    def load_projects(self):
        ''' Loads all of the projects from the database.
            
            Returns:
                A list of :class:`models.Project` objects.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def load_project(self, project_id):
        ''' Loads a project from the database.
            
            Args:
                project_id (int): The id of the project to retrieve from 
                the database.
            
            Returns:
                A :class:`models.Project` objects
                
                None if no project is located for the project_id.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def insert_project(self, project):
        ''' Inserts a non-existent project into the database.
            
            Args:
                project (:class:`models.Project`): The project to insert 
                into the database. The project's id will be ignored.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def update_project(self, project):
        ''' Updates an existing project in the database.
            
            Args:
                project (:class:`models.Project`): The project to update 
                in the database.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def delete_project(self, project_id):
        ''' Deletes an existing project from the database.
            
            Args:
                project_id (int): The id of the project to delete from 
                the database.
                
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def load_tasks(self, project_id):
        ''' Loads all of the tasks from the database.
            
            Args:
                project_id (int): The project id of the task to retrieve 
                from the database.
            
            Returns:
                A list of :class:`models.Task` objects.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def load_task(self, project_id, task_id):
        ''' Loads a task from the database based on the project_id and 
            task_id.
            
            Args:
                project_id (int): The project id of the task to retrieve 
                from the database.
                
                task_id (int): The id of the task to retrieve from the 
                database.
            
            Returns:
                A :class:`models.Task` object.
                
                None if no task is loaded for the project_id and task_id.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def insert_task(self, task):
        ''' Inserts a non-existent task into the database.
            
            Args:
                task (:class:`models.Task`): The task to insert 
                into the database. The task's id will be ignored.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def update_task(self, task):
        ''' Updates an existing task in the database.
            
            Args:
                task (:class:`models.Task`): The task to update 
                in the database.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def delete_task(self, project_id, task_id):
        ''' Deletes an existing task from the database.
            
            Args:
                project_id (int): The id of the task to delete from the 
                database.
                
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def load_login(self, username):
        ''' Loads a login from the database.
            
            Args:
                username (str): The username of the user to retrieve 
                from the database.
            
            Returns:
                A :class:`models.Login` object.
                
                None if no login is loaded for the username.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented
    
    @abstractmethod
    def initialize_database(self, username, password):
        ''' Initializes the database using a database-specific schema.
            
            Args:
                username (str): The username for the initial application user.
                password (str): The password for the initial application user.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        return NotImplemented

class DataCalculationError(Exception):
    ''' Database-agnostic error for calculation errors 
        (divide by 0, etc.).'''
    
    def __str__(self):
        '''Provides a string representation of the object.'''
        
        print('DataCalculationError: Error related to calculation.')

class DataIntegrityError(Exception):
    ''' Database-agnostic error for data integrity/constraint errors 
        (foreign key violation, etc.).'''
    
    def __str__(self):
        '''Provides a string representation of the object.'''
        
        print('DataIntegrityError: Error related to constraint violation.')

class PostgreSQL(Database):
    ''' Provides a database implementation for the PostgreSQL database.'''
    
    def open(self):
        ''' Opens the database connection.'''
        
        self._connection = psycopg2.connect(
            user = self.username,
            password = self.password,
            host = self.hostname,
            port = self.port,
            database = self.database_name
            )
    
    def close(self):
        ''' Closes the database connection.'''
        
        self._connection.close()
    
    def load_projects(self):
        ''' Loads all of the projects from the database.
            
            Returns:
                A list of :class:`models.Project` objects.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
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
        ''' Loads a project from the database.
            
            Args:
                project_id (int): The id of the project to retrieve from 
                the database.
            
            Returns:
                A :class:`models.Project` objects
                
                None if no project is located for the project_id.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
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
        ''' Inserts a non-existent project into the database.
            
            Args:
                project (:class:`models.Project`): The project to insert 
                into the database. The project's id will be ignored.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('INSERT INTO project (name, brief_description, '
               'description) VALUES (%s, %s, %s);')
        parameters = [project.name, project.brief_description, 
                      project.description]
        
        self._execute_non_query(sql, parameters)
    
    def update_project(self, project):
        ''' Updates an existing project in the database.
            
            Args:
                project (:class:`models.Project`): The project to update 
                in the database.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('UPDATE project SET name=%s, brief_description=%s, '
               'description=%s WHERE id=%s;')
        parameters = [project.name, project.brief_description, 
                      project.description, project.id]
        
        self._execute_non_query(sql, parameters)
    
    def delete_project(self, project_id):
        ''' Deletes an existing project from the database. Deletes any 
            tasks associated with the project as well.
            
            Args:
                project_id (int): The id of the project to delete from 
                the database.
                
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('DELETE FROM task WHERE project_id=%s;')
        parameters = [project_id]
        self._execute_non_query(sql, parameters)
        
        sql = ('DELETE FROM project WHERE id=%s;')
        parameters = [project_id]
        self._execute_non_query(sql, parameters)
    
    def load_tasks(self, project_id):
        ''' Loads all of the tasks from the database.
            
            Args:
                project_id (int): The project id of the task to retrieve 
                from the database.
            
            Returns:
                A list of :class:`models.Task` objects.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
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
        ''' Loads a task from the database.
            
            Args:
                project_id (int): The project id of the task to retrieve 
                from the database.
                
                task_id (int): The id of the task to retrieve from the 
                database.
            
            Returns:
                A :class:`models.Task` object.
                
                None if no task is loaded for the project_id and task_id.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
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
        ''' Inserts a non-existent task into the database.
            
            Args:
                task (:class:`models.Task`): The task to insert 
                into the database. The task's id will be ignored.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('INSERT INTO task (project_id, name, brief_description, '
               'description, complexity, due_date, status) VALUES '
               '(%s, %s, %s, %s, %s, %s, %s);')
        parameters = [task.project_id, task.name, task.brief_description, 
                      task.description, task.complexity.value, task.due_date, 
                      task.status.value]
        
        self._execute_non_query(sql, parameters)
        
    def update_task(self, task):
        ''' Updates an existing task in the database.
            
            Args:
                task (:class:`models.Task`): The task to update 
                in the database.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('UPDATE task SET project_id=%s, name=%s, '
               'brief_description=%s, description=%s, complexity=%s, '
               'due_date=%s, status=%s WHERE id=%s AND project_id=%s;')
        parameters = [task.project_id, task.name, task.brief_description, 
                      task.description, task.complexity.value, task.due_date, 
                      task.status.value, task.id, task.project_id]
        
        self._execute_non_query(sql, parameters)
        
    def delete_task(self, project_id, task_id):
        ''' Deletes an existing task from the database.
            
            Args:
                project_id (int): The id of the task to delete from the 
                database.
                
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('DELETE FROM task WHERE id=%s AND project_id=%s;')
        parameters = [task_id, project_id]
        
        self._execute_non_query(sql, parameters)
    
    def load_login(self, username):
        ''' Loads a login from the database.
            
            Args:
                username (str): The username of the user to retrieve 
                from the database.
            
            Returns:
                A :class:`models.Login` object.
                
                None if no login is loaded for the username.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        sql = ('SELECT id, username, password FROM login WHERE username=%s;')
        parameters = [username]
        
        rows = self._execute_query(sql, parameters)
        
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
    
    def initialize_database(self, username, password):
        ''' Initializes the database using a database-specific schema.
            
            Args:
                username (str): The username for the initial application user.
                password (str): The password for the initial application user.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        schema_name = 'postgresqlschema.sql'
        
        with open(schema_name, 'r') as schema_file:
            cursor = self._connection.cursor()
            
            try:
                rows = cursor.execute(schema_file.read())
                cursor.execute('INSERT INTO login(username, password) VALUES (%s, %s)',
                               [username, password])
                    
                self._connection.commit()
            except:
                print('Database schema already exists.')
    
    def _execute_query(self, sql, parameters):
        ''' Executes an SQL query that returns results.
            
            Args:
                sql (str): The query to execute.
                parameters ([]): A list of parameters for the query.
            
            Returns:
                A list of tuples representing the database rows returned 
                from the database.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        try:
            cursor = self._connection.cursor()
            cursor.execute(sql, parameters)
            rows = cursor.fetchall()
        except(psycopg2.IntegrityError):
            raise(DataIntegrityError)
        except(psycopg2.DataError):
            raise(DataCalculationError)
        
        return rows
    
    def _execute_non_query(self, sql, parameters):
        ''' Executes an SQL query that does not return results.
            
            Args:
                sql (str): The query to execute.
                parameters ([]): A list of parameters for the query.
            
            Raises:
                DataCalculationError: Calculation caused an exception 
                (divide by 0, etc.).
                
                DataIntegrityError: Constrain violation.'''
        
        try:
            cursor = self._connection.cursor()
            rows = cursor.execute(sql, parameters)
            self._connection.commit()
        except(psycopg2.IntegrityError):
            raise(DataIntegrityError)
        except(psycopg2.DataError):
            raise(DataCalculationError)

