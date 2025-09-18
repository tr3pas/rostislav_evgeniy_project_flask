
from flask import render_template, request, redirect, url_for, flash
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from settings import Session
from flask import Blueprint


bp = Blueprint('menu', __name__)


@bp.route("/")
def list_menu_items():
    with Session() as session:
        menu_items = session.query(User).all()
    return render_template("menu/list.html", menu_items=menu_items)


@bp.route("/menu/<int:item_id>")
def details_menu_item(item_id):
    with Session() as session:
        menu_item = session.query(User).get(item_id)
        if not menu_item:
            return "Menu item not found", 404
    return render_template("menu/details.html", menu_item=menu_item)