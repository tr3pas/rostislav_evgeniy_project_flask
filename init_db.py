from models import Base, User, Menu, Orders, Reservations
from settings import  Session
from werkzeug.security import generate_password_hash, check_password_hash


# Ініціалізація бази даних і додавання товарів
def init_db():
    base = Base()
    base.drop_db()
    base.create_db()  # Створюємо таблиці

    session = Session()
    user = User(username="admin", 
                email="admin@example.com", 
                hash_password=generate_password_hash("admin123"),
                is_admin=True)
    session.add(user)
    session.commit()


if __name__ == "__main__":
    init_db()
