import os
import uuid
from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import select

from models import Menu, Orders, User
from settings import Session, config

bp = Blueprint("admin", __name__)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401)  # Unauthorize
        if not getattr(current_user, "is_admin", False):
            return abort(403)  # Forbidden
        return func(*args, **kwargs)

    return wrapper


@bp.route("/", methods=["GET", "POST"])
@admin_required
def admin_panel():
    if request.method == "POST":
        pos_id = request.form.get("pos_id")
        with Session() as session:
            stmt = select(Menu).filter_by(id=pos_id)
            # stmt = select(Menu).where(Menu.id == pos_id)
            menu_pos = session.scalar(stmt)

            if "change_status" in request.form and menu_pos:
                menu_pos.active = not menu_pos.active

            elif "delete_position" in request.form and menu_pos:
                session.delete(menu_pos)

            elif "change_position" in request.form and menu_pos:
                redirect(url_for("admin.update_menu.<int:pos_id>", pos_id=pos_id))

            session.commit()

    with Session() as session:
        stmt = select(Menu)
        positions = session.scalars(stmt).all()

    return render_template(
        "administrate/admin_panel.html", title="Admin Panel", all_positions=positions
    )


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
    return render_template("administrate/create_menu.html", title="Create Menu Item")


@bp.route("/update_menu/<int:pos_id>", methods=["GET", "POST"])
@admin_required
def update_menu(pos_id):
    with Session() as session:
        stmt = select(Menu).filter_by(id=pos_id)
        # stmt = select(Menu).where(Menu.id == pos_id)
        menu_pos = session.scalar(stmt)

    return render_template(
        "administrate/update_menu.html", title="Change Menu Item", position=menu_pos
    )


@bp.route("/orders", methods=["GET", "POST"])
@admin_required
def all_orders():
    if request.method == "POST":
        order_id = request.form.get("order_id")
        with Session() as cursor:
            stmt = select(Orders).where(Orders.id == order_id)
            order = cursor.scalar(stmt)
            if order and order.status == "active":
                order.status = "completed"
                cursor.commit()
        return redirect(url_for("admin.all_orders"))

    with Session() as cursor:
        stmt = select(Orders, User).join(User, Orders.user_id == User.id)
        orders_results = cursor.execute(stmt).fetchall()

    return render_template("administrate/orders.html", orders_results=orders_results)


@bp.route("/users_control", methods=["GET", "POST"])
@admin_required
def users_control():
    if request.method == "POST":
        pos_id = request.form.get("pos_id")
        with Session() as session:
            stmt = select(User).filter_by(id=pos_id)
            # stmt = select(Menu).where(Menu.id == pos_id)
            menu_pos = session.scalar(stmt)
            if "delete_position" in request.form and menu_pos:
                session.delete(menu_pos)

            session.commit()

    with Session() as session:
        stmt = select(User)
        users = session.scalars(stmt).all()

    return render_template(
        "administrate/users_control.html", title="Users control", all_users=users
    )
