from flask import jsonify
from flask_mysql_connector import MySQL

class UserManager:
    def __init__(self, mysql):
        self.mysql = mysql

    @classmethod
    def init_db(cls, mysql):
        cls.mysql = mysql

    @classmethod
    def add_user(cls, user_id, email):
        cur = cls.mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO user (user_id, email) VALUES (%s, %s)",
                (user_id, email)
            )
            cls.mysql.connection.commit()
            print(f"User with ID '{user_id}' has been added.")
        except Exception as e:
            print(f"Error adding user in database: {str(e)}")

    @classmethod  # check if user exist in database
    def get_user_by_id(cls, user_id):
        cur = cls.mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM user WHERE user_id = %s",
            (user_id,)
        )
        user = cur.fetchone()
        return user
