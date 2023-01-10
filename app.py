import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

CREATE_ROOM_TABLE = "CREATE TABLE IF NOT EXISTS rooms (id SERIAL PRIMARY KEY, name TEXT);"
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (name) VALUES (%s) RETURNING id;"
ROOMS_DETAIL = "SELECT * FROM rooms"
DELETE_ROOM = "DELETE FROM rooms where id = %s"
UPDATE_ROOM = "UPDATE rooms set name = %s where id = %s"
load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URl")
connection = psycopg2.connect(url)


@app.route("/")
def start():
    return "First page of REST API"


@app.get("/api")
def get_room():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(ROOMS_DETAIL)
            data = []
            for record in cursor:
                temp = {
                    "id": record[0],
                    "room": record[1],
                }
                data.append(temp)
    return jsonify(data)


@app.post("/api/room")
def create_room():
    data = request.get_json()
    value = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOM_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (value,))
            room_id = cursor.fetchone()[0]
    return {"id": room_id, "message": f"Room {value} created."}, 201


@app.route("/api/room/<int:id>", methods=["DELETE"])
def delete_room(id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ROOM, (id,))
    return {"Deleted room with id ": id}


@app.route("/api/room/<string:val>/<int:id>", methods=["PUT"])
def update_room(val, id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_ROOM, (val, id))
    return {"Updated room with id ": id}
