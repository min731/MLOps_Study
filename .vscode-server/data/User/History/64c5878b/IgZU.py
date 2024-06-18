from flask import Blueprint

bp = Blueprint('check', __name__, url_prefix='/check')

@bp.route("/")
def print_check():
	return "hello check!"