from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

todos = []
next_id = 1


class TodoIn(BaseModel):
    title: str
    done: Optional[bool] = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos")
def list_todos():
    return todos


@app.post("/todos")
def create_todo(todo: TodoIn):
    global next_id
    new_todo = {"id": next_id, "title": todo.title, "done": False}
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    return [t for t in todos if t["id"] == todo_id][0]


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            del todos[i]
            return {"deleted": todo_id}
    return {"deleted": todo_id}
