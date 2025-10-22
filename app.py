from core import create_app, db
from api import register_routes as auth_routes
from meals import register_routes as meals_routes
import bcrypt
from flask_login import LoginManager, login_user, current_user,logout_user,login_required

app = create_app()

auth_routes(app)
meals_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)