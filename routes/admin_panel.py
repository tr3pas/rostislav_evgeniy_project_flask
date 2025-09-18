from functools import wraps
import uuid
from flask import abort, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models import Menu

from settings import Session, config
from flask import Blueprint

import os


bp = Blueprint('admin', __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)   # Unauthorized
        if not getattr(current_user, "is_admin", False):
            return abort(403)   # Forbidden

        return func(*args, **kwargs)
    return wrapper


@bp.route("/")
@admin_required
def admin_panel():
    return render_template("administrate/admin_panel.html", title="Admin Panel")


@bp.route("/create_menu", methods=["GET", "POST"])
@admin_required
def create_menu():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        description = request.form.get("description")
        category = request.form.get("category")
        
        image = request.files.get("image")

        if image:
            os.makedirs(config.IMAGES_DIR, exist_ok=True)

            unique_filename = f"{uuid.uuid4().hex}_{image.filename}"

            image_path = f"{config.IMAGES_DIR}/{unique_filename}"
            image.save(image_path)

        with Session() as session:
            menu_item = Menu(
                name=name,
                price=price,
                description=description,
                category=category,
                image_path=image_path if image else None,
            )
            session.add(menu_item)
            session.commit()

        flash("Menu created successfully!", "success")
        return redirect(url_for("admin.create_menu"))
    return render_template("administrate/create_menu.html",  title="Create Menu Item")

