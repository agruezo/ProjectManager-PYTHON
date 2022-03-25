from flask import render_template, redirect, session, request
from flask_app import app
from flask_app.models import project
from flask_app.models import user

@app.route('/projects')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    data = {
        'user_id': session['user_id']
    }

    logged_in_user = user.User.get_by_id(user_data)
    projects = project.Project.get_all_projects()
    project_joins = project.Project.get_all_project_joins(data)

    return render_template('allProjects.html', logged_in_user = logged_in_user, projects = projects, project_joins = project_joins)

@app.route('/projects/new')
def new_project():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    logged_in_user = user.User.get_by_id(data)
    return render_template('newProject.html', logged_in_user = logged_in_user)

@app.route('/projects/create', methods = ['POST'])
def create_project():
    if 'user_id' not in session:
        return redirect('/logout')
    if not project.Project.validate_project(request.form):
        return redirect('/projects/new')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form["due_date"],
        "user_id": request.form["leader"]
    }

    project.Project.create_project(data)
    return redirect('/projects')

@app.route('/projects/<int:id>')
def show_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id": session['user_id']
    }
    project_data = {
        "user_id": session['user_id']
    }
    data = {
        "id": id
    }

    logged_in_user = user.User.get_by_id(user_data)
    current_project = project.Project.show_project(data)
    project_joins = project.Project.get_all_project_joins(project_data)
    return render_template("showProject.html", logged_in_user = logged_in_user, current_project = current_project, project_joins = project_joins)

@app.route('/projects/<int:id>/edit')
def edit_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id'],
    }
    data = {
        "id": id
    }

    logged_in_user = user.User.get_by_id(user_data)
    current_project = project.Project.show_project(data)
    return render_template("editProject.html", logged_in_user = logged_in_user, current_project = current_project)

@app.route('/projects/<int:id>/update', methods=['POST'])
def update_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not project.Project.validate_project(request.form):
        return redirect(f'/projects/{id}/edit')
    data = {
        "id": id,
        "title": request.form["title"],
        "description": request.form["description"],
        "due_date": request.form["due_date"]
    }

    project.Project.update_project(data)
    return redirect('/projects')

@app.route('/projects/<int:id>/delete', methods=['POST'])
def delete_project(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    
    project.Project.destroy_project(data)
    return redirect('/projects')

@app.route('/projects/<int:id>/join')
def join_project(id):
    data = {
        "user_id": session['user_id'],
        "project_id": id
    }
    
    project.Project.add_project(data)
    return redirect('/projects')

@app.route('/projects/<int:id>/leave')
def leave_project(id):
    data = {
        "user_id": session['user_id'],
        "project_id": id
    }

    project.Project.remove_project(data)
    return redirect('/projects')

