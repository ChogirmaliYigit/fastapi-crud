from enum import Enum
from pydantic import BaseModel


class Category(BaseModel):
    title: str


class TaskStatus(str, Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class TaskPriority(str, Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Task(BaseModel):
    title: str
    description: str
    status: TaskStatus = None
    priority: TaskPriority = None
    category_id: int
