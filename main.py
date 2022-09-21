from pathlib import Path

from flask import Flask

app = Flask(__name__)
path_file = Path("file.txt")


@app.route("/")
def index():
    return "My Hometask"


@app.route("/requirements")
def file():
    return path_file.read_text()


if __name__ == "__main__":
    app.run(debug=True)
