from app import app, db
from flask import request, jsonify
from flask_login import login_required
from models import Task, User

from datetime import datetime

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.as_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    new_task = Task(
        title=data['title'],
        description=data['description'],
        due_date=due_date,
        category=data['category'],
        priority=data['priority'],
        user_id=data['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.as_dict())

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    data = request.json
    task = Task.query.get(task_id)
    task.title = data['title']
    task.description = data['description']
    task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    task.category = data['category']
    task.priority = data['priority']
    db.session.commit()
    return jsonify(task.as_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/tasks/filter', methods=['GET'])
@login_required
def filter_tasks():
    category = request.args.get('category')
    priority = request.args.get('priority')
    tasks = Task.query

    if category:
        tasks = tasks.filter_by(category=category)
    if priority:
        tasks = tasks.filter_by(priority=priority)

    return jsonify([task.as_dict() for task in tasks.all()])

@app.route('/api/tasks/search', methods=['GET'])
@login_required
def search_tasks():
    query = request.args.get('query', '')
    tasks = Task.query.filter(
        (Task.title.ilike(f'%{query}%')) | 
        (Task.description.ilike(f'%{query}%'))
    ).all()
    return jsonify([task.as_dict() for task in tasks])