from fastapi import FastAPI
from app.db import Database
from app.models import Category, Task


app = FastAPI()
db = Database()

db.create_categories_table()
db.create_tasks_table()


@app.get("/categories")
async def categories():
    return [{
        "id": category[0],
        "title": category[1],
    } for category in db.get_all_categories()]


@app.get("/category/{category_id}")
async def get_category(category_id: int):
    category = db.get_a_category(category_id)
    return {"id": category[0], "title": category[1]}


@app.post("/categories")
async def add_category(data: Category):
    db.add_a_category(data.title)
    return {"detail": "Category successfully added!"}


@app.put("/category/{category_id}")
async def update_category(category_id: int, data: Category):
    db.update_a_category(category_id, data.title)
    return {"detail": "Category successfully updated!"}


@app.delete("/category/{category_id}")
async def delete_category(category_id: int):
    db.delete_a_category(category_id)
    return {"detail": "Category successfully deleted!"}


@app.get("/tasks")
async def tasks(category_id: int = None):
    return [{
        "id": task[0],
        "title": task[1],
        "description": task[2],
        "status": task[3],
        "priority": task[4],
        "category_id": task[5],
    } for task in db.get_all_tasks(category_id)]


@app.get("/task/{task_id}")
async def get_task(task_id: int):
    task = db.get_a_task(task_id)
    print(task)
    return {
        "id": task[0],
        "title": task[1],
        "description": task[2],
        "status": task[3],
        "priority": task[4],
        "category_id": task[5],
    }


@app.post("/tasks")
async def add_task(data: Task):
    db.add_a_task(data.title, data.description, data.category_id, data.status, data.priority)
    return {"detail": "Task successfully added!"}


@app.put("/task/{task_id}")
async def update_task(task_id: int, data: Task):
    db.update_a_task(
        task_id=task_id,
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        category_id=data.category_id,
    )
    return {"detail": "Task successfully updated!"}


@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    db.delete_a_task(task_id)
    return {"detail": "Task successfully deleted!"}
