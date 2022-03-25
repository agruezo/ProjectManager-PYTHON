from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Task:

    db_name = "project_manager_python"

    def __init__(self,data):
        self.id = data['id']
        self.ticket = data['ticket']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.project_id=data['project_id']

    @classmethod
    def get_all_tasks(cls):
        query = "SELECT * FROM tasks"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results

    @classmethod
    def get_all_project_tasks(cls, data):
        query = "SELECT *, users.first_name AS creator FROM tasks "\
        "LEFT JOIN users on users.id = tasks.user_id "\
        "WHERE project_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def create_task(cls, data):
        query = "INSERT into tasks (ticket, user_id, project_id) VALUES (%(ticket)s, %(user_id)s, %(project_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def update_task(cls, data):
        query = "UPDATE tasks SET ticket = %(ticket)s WHERE ide = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def remove_task(cls, data):
        query = "DELETE FROM tasks WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @staticmethod
    def validate_task(task):
        is_valid = True
        if len(task['ticket']) < 1:
            is_valid = False
            flash("Task field can not be left blank","task")
        return is_valid