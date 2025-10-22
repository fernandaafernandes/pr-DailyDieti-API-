import bcrypt
from flask import request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from models.user import User
from core import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):
    @app.route('/cadastrar', methods=['POST'])
    def register_user():
        data = request.get_json()
        name = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if email and password: 
            hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
            existing_user = User.query.filter_by(username=email).first()
            if existing_user:
                return jsonify({'message': 'Usuário já existe!'}), 400
        

            new_user = User(username=name, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
        
        return jsonify({'message': 'Dados inválidos!'}), 400
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'Login realizado com sucesso!'}), 200
        
        return jsonify({'message': 'Credenciais inválidas!'}), 401
    
    @app.route('/logout', methods=['POST'])
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logout realizado com sucesso!'}), 200