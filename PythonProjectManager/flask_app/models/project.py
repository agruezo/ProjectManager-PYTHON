import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Project:

    db_name ="project_manager_python"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.due_date = data['due_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.users_who_join= []

    @classmethod
    def get_all_projects(cls):
        query = "SELECT projects.id, projects.title, users.first_name AS leader, projects.due_date FROM projects "\
        "JOIN users ON users.id = projects.user_id "\
        "LEFT JOIN joins ON projects.id = joins.project_id "\
        "GROUP BY projects.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results

    @classmethod
    def get_all_project_joins(cls, data):
        project_joins = []
        query = "SELECT project_id FROM joins WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        for result in results:
            project_joins.append(result['project_id'])
        return project_joins
    
    @classmethod
    def create_project(cls, data):
        query = "INSERT into projects (title, description, due_date, user_id) VALUES (%(title)s, %(description)s, %(due_date)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def show_project(cls, data):
        query = "SELECT *, projects.id AS project, users.first_name AS leader FROM projects "\
        "JOIN users ON users.id = projects.user_id "\
        "WHERE projects.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print (results[0])
        
        return (results[0])

    @classmethod
    def show_project_and_leader(cls, data):
        query = "SELECT *, users.first_name AS leader, projects.id AS project FROM users "\
        "LEFT JOIN projects ON users.id = projects.user_id "\
        "WHERE projects.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def update_project(cls, data):
        query = "UPDATE projects SET title = %(title)s, description = %(description)s, due_date = %(due_date)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def destroy_project(cls, data):
        query = "DELETE FROM projects WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def add_project(cls, data):
        query = "INSERT INTO joins (user_id, project_id) VALUES (%(user_id)s, %(project_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def remove_project(cls, data):
        query = "DELETE from joins WHERE user_id = %(user_id)s AND project_id = %(project_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_project(project):
        is_valid = True
        if len(project['title']) < 1:
            is_valid = False
            flash("Title field can not be left blank","project")
        if len(project['description']) < 1:
            is_valid = False
            flash("Description field can not be left blank","project")
        if len(project['due_date']) < 1:
            is_valid = False
            flash("Due date field can not be left blank","project")
        return is_valid