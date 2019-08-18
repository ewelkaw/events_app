from flask import Blueprint

from . import errors, views

main = Blueprint("main", __name__)
