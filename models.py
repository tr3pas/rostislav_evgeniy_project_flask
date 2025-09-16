from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings import Session

from flask_login import UserMixin

from settings import Base


class User(UserMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(200), nullable=False)

    is_admin: Mapped[bool] = mapped_column(default=False)


    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="user")
    reservations: Mapped[list["Reservations"]] = relationship("Reservations", back_populates="user")

    def __repr__(self) -> str:
        return f"User: {self.id}, {self.username}"
    
    @staticmethod
    def get(user_id: int) :
        with Session() as session:
            user = session.scalar(select(User).filter(User.id == user_id))
            return user
        

    @classmethod
    def get_by_username(cls, username: str) :
        with Session() as session:
            user = session.scalar(select(cls).filter(cls.username == username))
            return user
        

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

    orders: Mapped[list["Orders"]] = relationship("Orders", back_populates="orders_items")
    
    def __repr__(self) -> str:
        return f"Menu: {self.id}, {self.name}"


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    order_list: Mapped[list["Menu"]] = mapped_column(ForeignKey("menu.id"), nullable=False)  # JSON string of ordered items

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user: Mapped["User"] = relationship("User", foreign_keys="Orders.user_id", back_populates="orders")
    orders_items: Mapped[list["Menu"]] = relationship("Menu", foreign_keys="Orders.order_list", back_populates="orders")

    def __repr__(self) -> str:
        return f"Order: {self.id}, User ID: {self.user_id}"

class Reservations(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    user: Mapped["User"] = relationship("User", foreign_keys="Reservations.user_id", back_populates="reservations")


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