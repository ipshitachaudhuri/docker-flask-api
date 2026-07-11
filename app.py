import os
import psycopg2

from flask import Flask, request

app = Flask(__name__)


def get_db_connection():

    connection = psycopg2.connect(
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD")
    )

    return connection



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



@app.route("/")
def home():

    return {
        "message": "Hello from Docker Project!"
    }



@app.route("/health")
def health():

    return {
        "status": "healthy"
    }



@app.route("/version")
def version():

    return {
        "application": "flask-api",
        "version": "3.0.0",
        "environment": "development"
    }



@app.route("/db")
def database_test():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "database": "connected",
        "version": result[0]
    }



@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    name = data["name"]
    email = data["email"]


    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO users (name,email)
        VALUES (%s,%s)
        """,
        (name,email)
    )


    connection.commit()


    cursor.close()
    connection.close()


    return {
        "message": "User created"
    }



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



create_table()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )

