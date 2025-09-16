from flask import Flask,  render_template

from settings import DatabaseConfig, Session
from flask_login import LoginManager
from models import User
from routes import auth
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(DatabaseConfig)

login_manager = LoginManager()
login_manager.login_view = "login" # type: ignore
login_manager.init_app(app)

# csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    print(user)
    return user


@app.route("/")
def index():
    return render_template("index.html")

app.register_blueprint(auth.bp, url_prefix="/auth")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5050)
