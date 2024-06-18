from flask import Blueprint

// url prefix 지정
// 이제 아래에 생성되는 모든 route 경로는 앞에 "/blue"가 붙게 됨
bp = Blueprint('blue', __name__, url_prefix='/blue')

// /blue/1
@bp.route("/1")
def print_blue():
	return "hello Blue!"
[출처] [Flask 입문] Blueprint로 소스 코드를 나눠보자|작성자 IML

