import csv
import json
from pathlib import Path

import requests
from faker import Faker
from flask import Flask

fake = Faker()
app = Flask(__name__)
path_file = Path("file.txt")


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


@app.route('/space')
def space_json_reader():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    astronauts = response.text
    reader = json.loads(astronauts)
    return f"All astronauts = {reader['number']}"


@app.route('/mean')
def calculations():
    weight = 0
    height = 0
    dig = 0
    with open('people_data.csv', 'r', newline='') as csvfile:
        reading = csv.DictReader(csvfile)
        for i in reading:
            weight += float(list(i.values())[2]) * 0.45
            height += float(list(i.values())[1]) * 2.54
            dig += 1
        mid_weight = weight / dig
        mid_height = height / dig
        return (
            f'<li>Middle weight {round(mid_weight, 3)} kg'
            f'<li>Middle height {round(mid_height, 3)} cm'
        )


@app.route("/")
def index():
    return "My Hometask"


@app.route("/requirements")
def file():
    return path_file.read_text()


if __name__ == "__main__":
    app.run(debug=True)
