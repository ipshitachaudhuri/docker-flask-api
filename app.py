import os
import psycopg2

from flask import Flask, request

app = Flask(__name__)


def get_db_connection():

    return psycopg2.connect(
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD")
    )


def create_table():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()



@app.route("/health")
def health():

    return {
        "status": "healthy"
    }



@app.route("/db")
def db():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "database": "connected",
        "version": version[0]
    }



@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users(name,email)
        VALUES(%s,%s)
        """,
        (
            data["name"],
            data["email"]
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User created"
    }, 201



@app.route("/users", methods=["GET"])
def get_users():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id,name,email FROM users"
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
        for user in users
    ]



@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    connection = get_db_connection()
    cursor = connection.cursor()


    cursor.execute(
        "SELECT id FROM users WHERE id=%s",
        (user_id,)
    )

    user = cursor.fetchone()


    if user is None:

        cursor.close()
        connection.close()

        return {
            "error": "User not found"
        }, 404



    cursor.execute(
        """
        UPDATE users
        SET name=%s,
            email=%s
        WHERE id=%s
        """,
        (
            data["name"],
            data["email"],
            user_id
        )
    )


    connection.commit()

    cursor.close()
    connection.close()


    return {
        "message": "User updated"
    }



@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    connection = get_db_connection()
    cursor = connection.cursor()


    cursor.execute(
        "SELECT id FROM users WHERE id=%s",
        (user_id,)
    )


    user = cursor.fetchone()


    if user is None:

        cursor.close()
        connection.close()

        return {
            "error": "User not found"
        }, 404



    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )


    connection.commit()

    cursor.close()
    connection.close()


    return {
        "message": "User deleted"
    }



create_table()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )

