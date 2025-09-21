
from flask import render_template
from flask import Blueprint


bp = Blueprint('error', __name__)


@bp.errorhandler(403)
def forbidden_error(error):
    return render_template("errors/403.html")

@bp.errorhandler(404)
def forbidden_error(error):
    return render_template("errors/403.html")

@bp.errorhandler(401)
def forbidden_error(error):
    return render_template("errors/403.html")

@bp.errorhandler(500)
def forbidden_error(error):
    return render_template("errors/403.html")