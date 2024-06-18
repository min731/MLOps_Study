from flask import Blueprint

bp = Blueprint('blue', __name__, url_prefix='/check')

@bp.route("/1")
def print_blue():
	return "hello Blue!"