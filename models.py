from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings import Base, Session


class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(200), nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False)

    orders: Mapped[list["Orders"]] = relationship(
        "Orders", back_populates="user", cascade="all, delete-orphan"
    )
    reservations: Mapped[list["Reservations"]] = relationship(
        "Reservations", back_populates="user"
    )

    def __repr__(self) -> str:
        return f"User: {self.id}, {self.username}"

    @staticmethod
    def get(user_id: int):
        with Session() as session:
            user = session.scalar(select(User).filter(User.id == user_id))
            return user

    @classmethod
    def get_by_username(cls, username: str):
        with Session() as session:
            user = session.scalar(select(cls).filter(cls.username == username))
            return user


class OrderMenu(Base):
    __tablename__ = "orders_menu"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    order: Mapped["Orders"] = relationship(
        back_populates="order_items", lazy="selectin"
    )
    menu: Mapped["Menu"] = relationship(back_populates="menu_orders", lazy="selectin")

    def __repr__(self) -> str:
        return f"menu: {self.menu.name}, Quantity: {self.quantity}"


class Menu(Base):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=True, default=5)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    menu_orders: Mapped[list["OrderMenu"]] = relationship(
        back_populates="menu", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Menu: {self.id}, {self.name}"


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[str] = mapped_column(
        String(50), default="active"
    )  # active, completed, canceled

    # many-to-many
    order_items: Mapped[list["OrderMenu"]] = relationship(
        back_populates="order", lazy="selectin", cascade="all, delete-orphan"
    )

    user: Mapped["User"] = relationship(
        "User", foreign_keys="Orders.user_id", back_populates="orders"
    )

    def __repr__(self) -> str:
        return f"Order: {self.id},positions: {self.order_items}"

    @staticmethod
    def get(id_order: int):
        with Session() as session:
            order = session.scalar(select(Orders).filter(Orders.id == id_order))
            return order

    @classmethod
    def total_price_order(cls, order: "Orders") -> float:
        """Подсчитать общую стоимость заказа"""
        return sum(item.menu.price * item.quantity for item in order.order_items)


class Reservations(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user: Mapped["User"] = relationship(
        "User", foreign_keys="Reservations.user_id", back_populates="reservations"
    )

    def __repr__(self) -> str:
        return f"Reservation: {self.id}, User ID: {self.user_id}, Time Start: {self.time_start}"


# class Reviews(Base):
#     __tablename__ = "reviews"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#     rating: Mapped[int] = mapped_column(nullable=False)
# comment: Mapped[str] = mapped_column(String(500), nullable=True)

# user: Mapped["User"] = relationship()

# def __repr__(self) -> str:
#     return f"Review: {self.id}, User ID: {self.user_id}, Rating: {self.rating}"
