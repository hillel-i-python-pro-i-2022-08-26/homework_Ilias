from pathlib import Path

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


@app.route("/")
def index():
    return "My Hometask"


@app.route("/requirements")
def file():
    return path_file.read_text()


if __name__ == "__main__":
    app.run(debug=True)
