import csv
import json

import requests
from faker import Faker
from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.services.db_tab import table
from application.services.dbconnection import DbConnection
from application.settings import path_file

fake = Faker()
app = Flask(__name__)


def users():
    name = fake.first_name()
    mail = f"{str(name.lower())}_@gmail.com"
    yield f"{name}: {mail}"


# route_users_generate_by_number__start
@app.route("/generate-users/<int:quantity>")
@app.route("/generate-users/")
def generated_users(quantity: int = 100):
    num = quantity
    for i in range(num):
        for name in users():
            yield f"<p>{i + 1}. {name}</p>"


@app.route("/space")
def space_json_reader():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    astronauts = response.text
    reader = json.loads(astronauts)
    return f"All astronauts = {reader['number']}"


@app.route("/mean")
def calculations():
    weight = 0
    height = 0
    dig = 0
    with open("people_data.csv", "r", newline="") as csvfile:
        reading = csv.DictReader(csvfile)
        for i in reading:
            weight += float(list(i.values())[2]) * 0.45
            height += float(list(i.values())[1]) * 2.54
            dig += 1
        mid_weight = weight / dig
        mid_height = height / dig
        return (
            f"<li>Middle weight {round(mid_weight, 3)} kg"
            f"<li>Middle height {round(mid_height, 3)} cm"
        )


@app.route("/")
def index():
    return "My Hometask"


@app.route("/users/create-users")
@use_args(
    {"name": fields.Str(required=True), "number": fields.Int(required=True)},
    location="query",
)
def new_user(args):
    with DbConnection() as connection:
        with connection:
            connection.execute(
                """
            INSERT INTO phones(contactName, phoneNumber)
            VALUES (:contactName,:phoneNumber);
            """,
                dict(contactName=args["name"], phoneNumber=args["number"]),
            )
    return "User has been created HALI LUYA"


# создание новой строки с вытягиванием данных из базы
@app.route("/users/view-users")
def view():
    with DbConnection() as connection:
        mob_table = connection.execute(
            """
        SELECT * FROM phones;
        """
        ).fetchall()
    # беру данные из колонок таблицы и вставляю в новую строку с помощью джоина и переношу каждую последующую
    # итерацию на новую строку с помощью тега HTML бр

    return "<br>".join(
        [
            f"{user['phoneID']}. Name: {user['contactName']}. Number: {user['phoneNumber']} "
            for user in mob_table
        ]
    )


@app.route("/users/unique-user/<int:unique_id>")
def unique_user(unique_id):
    with DbConnection() as connection:
        solo_user = connection.execute(
            """
        SELECT * FROM phones 
        WHERE (phoneID=:unique_id);
        """,
            {"unique_id": unique_id},
        ).fetchone()
    return f"{solo_user['phoneID']}. Name:{solo_user['contactName']}. Number: {solo_user['phoneNumber']}"


@app.route("/users/update/<int:unique_id>")
@use_args(
    {"name": fields.Str(), "number": fields.Int()},
    location="query",
)
def update_user(args, unique_id):
    with DbConnection() as connection:
        with connection:
            name = args.get("name")
            number = args.get("number")
            if name is None and number is None:
                return Response("You didn`t choose argument", status=409)
            data = []
            if name is not None:
                data.append('contactName=:name')
            if number is not None:
                data.append('phoneNumber=:number')
            connection.execute(
                "UPDATE phones "
                f'SET {", ".join(data)} '
                "WHERE phoneID=:unique_id;",
                {"unique_id": unique_id,
                 "name": name,
                 "number": number}, )
    return 'Update complited'


@app.route("/users/delete/<int:unique_id>")
def delete_user(unique_id):
    with DbConnection() as connection:
        with connection:
            connection.execute("""
            DELETE FROM phones WHERE phoneID=:unique_id;
            """, {"unique_id": unique_id
                  })
    return 'user has been deleted'


@app.route("/requirements")
def file():
    return path_file.read_text()


table()

if __name__ == "__main__":
    app.run(debug=True)
