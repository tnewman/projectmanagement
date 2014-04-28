# File: model.py
# Description: Provides entity classes that represent the physical 
#              entities of the Project Management application.
# Date: 2014/04/27
# Programmer: Thomas Newman

''' Provides entity classes that represent the physical entities of the 
    Project Management application. '''

from datetime import datetime
from enum import Enum

class Complexity(Enum):
    ''' Represents the task complexity.'''
    
    #: The task complexity is unknown.
    UNKNOWN = 'Unknown'
    #: The task complexity is low.
    LOW = 'Low'
    #: The task complexity is medium.
    MEDIUM = 'Medium'
    #: The task complexity is high.
    HIGH = 'High'


class Status(Enum):
    ''' Represents the class status.'''
    
    #: The task status is unknown.
    UNKNOWN = 'Unknown'
    #: The task has not been started.
    NOT_STARTED = 'Not Started'
    #: The task is in-progress.
    IN_PROGRESS = 'In-Progress'
    #: The task has been completed.
    COMPLETE = 'Complete'

class Project:
    ''' Represents a project.'''
    
    def __init__(self):
        ''' Constructor'''
        self._id = 0 
        self._name = ''
        self._brief_description = ''
        self._description = ''
    
    @property
    def id(self):
        ''' (int): The non-negative id of the project in the database. '''
        return self._id
        
    @id.setter
    def id(self, value):
        # Ids must be int types
        if not isinstance(value, int):
            raise ValueError('id must be an integer')
        
        # Only allow positive ids
        if value < 0:
            raise ValueError('id must be positive')
        
        self._id = value
    
    @property
    def name(self):
        ''' (str): The name of the project. '''
        return self._name
    
    @name.setter
    def name(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('name must be a string')
        
        self._name = value
    
    @property
    def brief_description(self):
        ''' (str): A brief description of the project. '''
        return self._brief_description
    
    @brief_description.setter
    def brief_description(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('brief_description must be a string')
        
        self._brief_description = value
    
    @property
    def description(self):
        ''' (str): A full description of the project. '''
        return self._description
    
    @description.setter
    def description(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('description must be a string')
        
        self._description = value


class Task:
    ''' Represents a task.'''
    
    def __init__(self):
        ''' Constructor'''
        
        self._id = 0
        self._project_id = 0
        self._name = ''
        self._brief_description = ''
        self._description = ''
        self._complexity = Complexity.LOW
        self._due_date = datetime.now()
        self._status = Status.NOT_STARTED
        
    @property
    def id(self):
        ''' (int): The non-negative id of the task in the database. '''
        
        return self._id
    
    @id.setter
    def id(self, value):
        # Ids must be int types
        if not isinstance(value, int):
            raise ValueError('id must be an integer')
        
        # Only allow positive ids
        if value < 0:
            raise ValueError('id must be positive')
        
        self._id = value
    
    @property
    def project_id(self):
        ''' (int): The non-negative id of the project this task is 
            associated with in the database. '''
        
        return self._project_id
    
    @project_id.setter
    def project_id(self, value):
        # Ids must be int types
        if not isinstance(value, int):
            raise ValueError('project_id must be an integer')
    
        # Only allow positive ids
        if value < 0:
            raise ValueError('project_id must be positive')
        
        self._project_id = value
    
    @property
    def name(self):
        ''' (str): The name of the task. '''
        
        return self._name
    
    @name.setter
    def name(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('name must be a string')
        
        self._name = value
    
    @property
    def brief_description(self):
        ''' (str): A brief description of the task. '''
        
        return self._brief_description
    
    @brief_description.setter
    def brief_description(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('name must be a string')
        
        self._brief_description = value
    
    @property
    def description(self):
        ''' (str): A full description of the task. '''
        
        return self._description
    
    @description.setter
    def description(self, value):
        # Only allow string types
        if not isinstance(value, str):
            raise ValueError('name must be a string')
        
        self._description = value
    
    @property
    def complexity(self):
        ''' (:class:`Complexity`): The complexity of the task. '''
        
        return self._complexity
    
    @complexity.setter
    def complexity(self, value):
        # Coerce the value into a Complexity enum
        self._complexity = Complexity(value)
    
    @property
    def due_date(self):
        ''' (datetime.datetime): The date when the task is due. '''
        
        return self._due_date
    
    @due_date.setter
    def due_date(self, value):
        # Accept datetime types
        if isinstance(value, datetime):
            self._due_date = value
        else:
            try:
                # Parse the date if it is formatted as YY-MM-DD HH:MM:SS
                self._due_date = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except(ValueError):
                # Parse the date if it is formatted as YY-MM-DD
                self._due_date = datetime.strptime(value, '%Y-%m-%d')
    
    @property
    def status(self):
        ''' (:class:`Status`): The completion status of the task. '''
        
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = Status(value)
    
    def is_task_past_due(self):
        ''' Determines whether or not the task is past due.
        
        Returns:
            True -- The task is past due.
            False -- The task is not past due. '''
    
        # The task is past due if the current date is beyond the due date 
        # and the status is not complete.
        return self.due_date < datetime.now() and self.status != Status.COMPLETE


class Login:
    ''' Represents a login.'''
    
    def __init__(self):
        ''' Constructor'''
        
        self._id = 0
        self._username = ''
        self._password = ''
        
    @property
    def id(self):
        ''' (int): The id of the user in the database. '''
        
        return self._id
    
    @id.setter
    def id(self, value):
        # Only allow int types for ids
        if not isinstance(value, int):
                raise ValueError('id must be an integer')
        
        # Do not allow negative ids
        if value < 0:
            raise ValueError('id must be positive')
        
        self._id = value
    
    @property
    def username(self):
        ''' (str): The user's username. '''
        
        return self._username
    
    @username.setter
    def username(self, value):
        # Only allow string types for passwords
        if not isinstance(value, str):
            raise ValueError('username must be a string')
        
        self._username = value
    
    @property
    def password(self):
        ''' (str): The user's password (hashed and salted). '''
        
        return self._password
    
    @password.setter
    def password(self, value):
        # Only allow string types for passwords
        if not isinstance(value, str):
            raise ValueError('password must be a string')
        
        self._password = value
    
    def check_login(self, username, password):
        # No blank username or password allowed
        if username == '' or password == '':
            return False
        
        return self.username == username and self.password == password

