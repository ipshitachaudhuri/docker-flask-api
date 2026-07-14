import os
import time
import psycopg2

from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():

    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "postgres-db"),
        database=os.getenv("DATABASE_NAME", "postgres"),
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "postgres")
    )


def create_table():

    retries = 10

    for i in range(retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            """)

            conn.commit()
            cursor.close()
            conn.close()
            return

        except Exception:
            time.sleep(3)

    raise Exception("Database unavailable")


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


@app.route("/db")
def database():

    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "database": "connected"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



@app.route("/users", methods=["POST"])
def create_user():

    data = request.json

    name = data.get("name")

    if not name:
        return jsonify({
            "error": "name required"
        }), 400


    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO users(name)
        VALUES(%s)
        RETURNING id,name
        """,
        (name,)
    )


    user = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()


    return jsonify({
        "id": user[0],
        "name": user[1]
    }),201



@app.route("/users", methods=["GET"])
def get_users():

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT id,name FROM users ORDER BY id"
    )

    users = cursor.fetchall()


    cursor.close()
    conn.close()


    return jsonify([
        {
            "id":u[0],
            "name":u[1]
        }
        for u in users
    ])




@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data=request.json

    name=data.get("name")


    conn=get_db_connection()
    cursor=conn.cursor()


    cursor.execute(
        """
        UPDATE users
        SET name=%s
        WHERE id=%s
        RETURNING id,name
        """,
        (name,user_id)
    )


    user=cursor.fetchone()


    if not user:
        cursor.close()
        conn.close()

        return jsonify({
            "error":"user not found"
        }),404


    conn.commit()

    cursor.close()
    conn.close()


    return jsonify({
        "id":user[0],
        "name":user[1]
    })





@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    conn=get_db_connection()
    cursor=conn.cursor()


    cursor.execute(
        """
        DELETE FROM users
        WHERE id=%s
        RETURNING id
        """,
        (user_id,)
    )


    user=cursor.fetchone()


    if not user:

        cursor.close()
        conn.close()

        return jsonify({
            "error":"user not found"
        }),404


    conn.commit()

    cursor.close()
    conn.close()


    return jsonify({
        "message":"deleted"
    })




create_table()


if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=8000
    )

