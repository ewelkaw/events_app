from . import app, db
from .model import Event, WebSource


@app.route("/", methods=["GET"])
def index():
    return "X"
