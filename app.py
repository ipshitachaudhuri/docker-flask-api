import os
import psycopg2

from flask import Flask, request, jsonify

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )


def create_table():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/db")
def database_check():
    try:
        conn = get_db_connection()
        conn.close()

        return jsonify({
            "database": "connected"
        }), 200

    except Exception as e:
        return jsonify({
            "database": "failed",
            "error": str(e)
        }), 500


@app.route("/users", methods=["POST"])
def create_user():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        RETURNING id;
        """,
        (name, email)
    )

    user_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": user_id,
        "name": name,
        "email": email
    }), 201


@app.route("/users", methods=["GET"])
def get_users():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email FROM users ORDER BY id;"
    )

    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }
        for user in users
    ]), 200


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET name=%s, email=%s
        WHERE id=%s
        RETURNING id;
        """,
        (name, email, user_id)
    )

    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user_id,
        "name": name,
        "email": email
    }), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM users
        WHERE id=%s
        RETURNING id;
        """,
        (user_id,)
    )

    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "User deleted"
    }), 200


create_table()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )

