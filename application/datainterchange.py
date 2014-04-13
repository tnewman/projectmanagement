from datetime import datetime, timezone
from enum import Enum

class Complexity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

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
        self.complexity = Complexity.LOW
        self.due_date = datetime.now(timezone.utc)


class Login:
    def __init__(self):
        self.id = 0
        self.username = ''
        self.password = ''

