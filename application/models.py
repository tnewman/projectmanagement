from datetime import datetime, timezone
from enum import Enum

class Complexity(Enum):
    ''' Represents the task complexity.'''
    
    #: The task complexity is unknown.
    UNKNOWN = 'UNKNOWN'
    #: The task complexity is low.
    LOW = 'LOW'
    #: The task complexity is medium.
    MEDIUM = 'MEDIUM'
    #: The task complexity is high.
    HIGH = 'HIGH'


class Status(Enum):
    ''' Represents the class status.'''
    
    #: The task status is unknown.
    UNKNOWN = 'UNKNOWN'
    
    #: The task has not been started.
    NOT_STARTED = 'NOT_STARTED'
    
    #: The task is in-progress.
    IN_PROGRESS = 'IN_PROGRESS'
    
    #: The task has been completed.
    COMPLETE = 'COMPLETE'

class Project:
    ''' Represents a project.'''
    
    def __init__(self):
        ''' Constructor'''
        
        #: The id of the project in the database.
        self.id = 0
        
        #: The name of the project.
        self.name = ''
        
        #: A brief description of the project.
        self.brief_description = ''
        
        #: A full description of the project.
        self.description = ''


class Task:
    ''' Represents a task.'''
    
    def __init__(self):
        ''' Constructor'''
        
        #: (int): The id of the task in the database.
        self.id = 0
        
        #: (int): The id of the project this task is associated with in the 
        #: database.
        self.project_id = 0
        
        #: (str): The name of the task.
        self.name = ''
        
        #: (str): A brief description of the task.
        self.brief_description = ''
        
        #: (str): A full description of the task.
        self.description = ''
        
        #: (:class:`Complexity`): The complexity of the task.
        self.complexity = Complexity.UNKNOWN
        
        #: (datetime.datetime): The date when the task is due.
        self.due_date = datetime.now(timezone.utc)
        
        #: (:class:`Status`): The completion status of the task.
        self.status = Status.UNKNOWN


class Login:
    ''' Represents a login.'''
    
    def __init__(self):
        ''' Constructor'''
        
        #: (int): The id of the user in the database.
        self.id = 0
        
        #: (str): The user's username.
        self.username = ''
        
        #: (str): The user's password (hashed and salted).
        self.password = ''

