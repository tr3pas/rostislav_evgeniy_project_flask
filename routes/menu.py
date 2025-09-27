from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from sqlalchemy import select

from models import Menu, User
from settings import Session

bp = Blueprint("menu", __name__)


@bp.route("/menu")
def list_menu_items():
    with Session() as session:
        menu_items = session.scalars(select(Menu).filter_by(active=True))

        menu_items_list = [
            {"id": i.id, "name": i.name, "price": i.price, "image_path": i.image_path}
            for i in menu_items
        ]
        print(menu_items_list)
    return render_template(
        "menu/list.html", menu_items=menu_items_list, title="Menu IZI"
    )


@bp.route("/<int:item_id>")
def details_menu_item(item_id):
    with Session() as session:
        menu_item = session.scalar(select(Menu).where(Menu.id == item_id))
        if not menu_item:
            return abort(404)
    return render_template("menu/details.html", menu_item=menu_item)


@bp.route("/order/add/<int:item_id>", methods=["POST"])
@login_required
def add_to_order(item_id):
    quantity = request.form.get("quantity", 1, type=int)

    if "basket" not in session:
        basket: dict = {}
        basket[str(item_id)] = quantity
        session["basket"] = basket
    else:

        basket = session.get("basket", {})
        basket[str(item_id)] = quantity

    flash(f"позицію {item_id} додано до кошика")
    return redirect(url_for("menu.details_menu_item", item_id=item_id))
