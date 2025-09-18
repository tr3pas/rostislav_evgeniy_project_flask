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
                hash_password=generate_password_hash("admin"),
                is_admin=True)
    
    user2 = User(username="user", 
                email="user@example.com", 
                hash_password=generate_password_hash("user"),
                )
    
    m1 = Menu(
        name="Гункани з тунцем",
        price=150.00,
        rating=4,
        description="4 шт., тунець, ікра тобіко, майонез",
        image_path=None,
        category="Гункани",
        active=True
        )


    session.add_all([user, user2, m1])  
    session.commit()

    session.close()


if __name__ == "__main__":
    init_db()
