from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from models import Menu, OrderMenu, Orders, User
from settings import Session

bp = Blueprint("orders", __name__)


@bp.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    basket = session.get("basket", {})

    if not basket:
        flash("Your basket is empty!", "warning")
        return render_template("account/basket.html")

    menu_ids = list(basket.keys())
    quantities = basket.values()

    with Session() as db_session:
        menu_items = db_session.scalars(
            select(Menu).filter(Menu.id.in_(menu_ids))
        ).all()

    if request.method == "POST":
        with Session() as db_session:
            order = Orders(user_id=current_user.id)
            db_session.add(order)
            db_session.flush()  # получаем order.id сразу

            # Добавляем связки OrderMenu с количеством

            for menu, qty in zip(menu_items, quantities):
                db_session.add(
                    OrderMenu(order_id=order.id, menu_id=menu.id, quantity=int(qty))
                )

            db_session.commit()

            session["basket"] = {}
            flash("Order created successfully!", "success")

            return redirect(url_for("orders.order_details", order_id=order.id))

    return render_template(
        "account/basket.html", basket=dict(zip(menu_items, quantities))
    )


@bp.route("/clear_basket", methods=["POST"])
def clear_basket():
    session["basket"] = {}
    flash("Basket cleared!")
    return redirect(url_for("menu.list_menu_items"))


@bp.route("/order/<int:order_id>")
@login_required
def order_details(order_id):
    with Session() as session:
        order = session.scalar(select(Orders).filter(Orders.id == order_id))
        if not order:
            flash("Order not found!", "danger")
            return redirect(url_for("menu.menu_view"))

        total_price = Orders.total_price_order(order)

    return render_template(
        "account/orders_details.html", order=order, total_price=total_price
    )


@bp.route("/my_orders")
@login_required
def order_history():
    with Session() as session:
        user = session.merge(current_user)
        orders = user.orders
        print(orders)

        # todo

    return render_template("account/history_orders.html", orders=orders)


@bp.route("/cancel_order/<int:order_id>", methods=["POST"])
@login_required
def delete_order(order_id):
    with Session() as session:
        order = session.scalar(select(Orders).filter(Orders.id == order_id))
        if order:
            session.delete(order)
            session.commit()
    return redirect(url_for("orders.order_history"))
