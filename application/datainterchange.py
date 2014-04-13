from datetime import datetime, timezone
from enum import Enum

class Complexity(Enum):
    UNKNOWN = 'UNKNOWN'
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class Status(Enum):
    UNKNOWN = 'UNKNOWN'
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETE = 'COMPLETE'

class Project:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.brief_description = ''
        self.description = ''


class Task:
    def __init__(self):
        self.id = 0
        self.project_id = 0
        self.name = ''
        self.brief_description = ''
        self.description = ''
        self.complexity = Complexity.UNKNOWN
        self.due_date = datetime.now(timezone.utc)
        self.status = Status.UNKNOWN


class Login:
    def __init__(self):
        self.id = 0
        self.username = ''
        self.password = ''

