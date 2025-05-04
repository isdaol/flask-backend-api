from flask import Flask
from config import Config
from models import db
from views.auth import auth_bp, login_manager
from views.main import main_bp
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.login_message_category = 'info'

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)