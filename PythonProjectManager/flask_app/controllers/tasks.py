from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import project, user, task

@app.route('/projects/<int:id>/tasks')
def new_task(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    project_id = {
        'id': id
    }

    logged_in_user = user.User.get_by_id(data)
    current_project = project.Project.show_project_and_leader(project_id)
    current_tasks = task.Task.get_all_project_tasks(project_id)

    return render_template('projectTask.html', logged_in_user=logged_in_user, current_project=current_project, current_tasks=current_tasks)

@app.route('/projects/<int:id>/tasks/create', methods = ['POST'])
def create_task(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not task.Task.validate_task(request.form):
        return redirect(f'/projects/{id}/tasks')
    data = {
        "ticket": request.form["ticket"],
        "user_id": request.form["creator"],
        "project_id": request.form["project_task"]
    }
    task.Task.create_task(data)
    return redirect(f'/projects/{id}/tasks')

@app.route('/projects/<int:id>/tasks/<int:id2>/delete', methods = ['POST'])
def complete_task(id, id2):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id2
    }

    task.Task.remove_task(data)
    return redirect(f'/projects/{id}/tasks')