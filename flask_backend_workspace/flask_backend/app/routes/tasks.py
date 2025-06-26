from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models import db, Task, User
from app.schemas import TaskInputSchema, TaskSchema
from app.auth_utils import decode_token

blp = Blueprint(
    "Tasks",
    "tasks",
    url_prefix="/api/tasks",
    description="Endpoints for user task CRUD operations"
)

def get_current_user_id():
    """Helper to fetch current user_id from Authorization Bearer token."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, message="Authorization header missing or invalid.")
    token = auth_header.replace("Bearer ", "", 1)
    user_id = decode_token(token)
    if not user_id:
        abort(401, message="Invalid or expired authentication token.")
    return user_id

# PUBLIC_INTERFACE
@blp.route("/")
class TaskList(MethodView):
    """Create new task or list user's tasks"""
    @blp.arguments(TaskInputSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        user_id = get_current_user_id()
        task = Task(
            user_id=user_id, 
            title=task_data["title"], 
            description=task_data.get("description", ""), 
            completed=task_data.get("completed", False)
        )
        db.session.add(task)
        db.session.commit()
        return task

    @blp.response(200, TaskSchema(many=True))
    def get(self):
        user_id = get_current_user_id()
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        return tasks

# PUBLIC_INTERFACE
@blp.route("/<int:task_id>")
class TaskDetail(MethodView):
    """Get, update, or delete a task for current user"""
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        user_id = get_current_user_id()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            abort(404, message="Task not found.")
        return task

    @blp.arguments(TaskInputSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        user_id = get_current_user_id()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            abort(404, message="Task not found.")
        task.title = task_data.get("title", task.title)
        task.description = task_data.get("description", task.description)
        task.completed = task_data.get("completed", task.completed)
        db.session.commit()
        return task

    @blp.response(204)
    def delete(self, task_id):
        user_id = get_current_user_id()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            abort(404, message="Task not found.")
        db.session.delete(task)
        db.session.commit()
        return "", 204
