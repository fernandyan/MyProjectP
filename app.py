import os
from datetime import datetime

import stripe
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import generate_csrf

from blueprints.admin import admin_bp
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp
from blueprints.loja import loja_bp
from blueprints.main import main_bp, perfil
from models import User, db

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "sqlite:///portfolio.db"
)
app.config["STRIPE_SECRET_KEY"] = os.getenv("STRIPE_SECRET_KEY", "")
app.config["STRIPE_PUBLISHABLE_KEY"] = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
app.config["BASE_URL"] = os.getenv("BASE_URL", "http://127.0.0.1:5000")

stripe.api_key = app.config["STRIPE_SECRET_KEY"]

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year, "perfil": perfil, "csrf_token": generate_csrf}


app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(loja_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
