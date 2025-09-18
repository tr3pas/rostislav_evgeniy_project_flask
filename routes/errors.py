
from flask import render_template
from flask import Blueprint


bp = Blueprint('error', __name__)


@bp.errorhandler(403)
def forbidden_error(error):
    return render_template("errors/403.html")