from flask import request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import meals
from models.meal import Meal
from core import db

def register_routes(app):
    @app.route('/meals', methods=['POST'])
    @login_required
    def create_meal():
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        calories = data.get('calories')
        when_at = data.get('when_at')
        in_diet = data.get('in_diet')
        if name and calories and when_at:
            new_meal = Meal(
                name=name,
                description=description,
                calories=calories,
                when_at=when_at,
                in_diet=in_diet,
                user_id=current_user.id
            )
            db.session.add(new_meal)
            db.session.commit()
            return jsonify({'message': 'Refeição criada com sucesso!!'}), 201
        
    @app.route('/meals/id/<int:meal_id>', methods=['PUT'])
    @login_required
    def update_meal(meal_id):
        data = request.get_json()
        meal = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
        if not meal:
            return jsonify({'message': 'Refeição não encontrada!'}), 404
        
        meal.name = data.get('name', meal.name)
        meal.description = data.get('description', meal.description)
        meal.calories = data.get('calories', meal.calories)
        meal.when_at = data.get('when_at', meal.when_at)
        meal.in_diet = data.get('in_diet', meal.in_diet)
        
        db.session.commit()
        return jsonify({'message': 'Refeição atualizada com sucesso!'}), 200
    
    @app.route('/meals/id/<int:meal_id>', methods=['DELETE'])
    @login_required
    def delete_meal(meal_id):
        meals = Meal.query.filter_by(id=meal_id, user_id=current_user.id).first()
        if not meals:
            return jsonify({'message': 'Refeição não encontrada!'}), 404
        
        db.session.delete(meals)
        db.session.commit()
        return jsonify({'message': 'Refeição deletada com sucesso!'}), 200
    
    @app.route('/meals', methods=['GET'])
    @login_required
    def get_meals():
        meals = Meal.query.filter_by(user_id=current_user.id).all()
        meals_list = []
        for meal in meals:
            meals_list.append({
                'id': meal.id,
                'name': meal.name,
                'description': meal.description,
                'calories': meal.calories,
                'when_at': meal.when_at,
                'in_diet': meal.in_diet,
                'created_at': meal.created_at,
                'updated_at': meal.updated_at
            })
        return jsonify(meals_list), 200
    
    @app.route('/meals/user/<int:user_id>', methods=['GET'])
    @login_required
    def get_meals_by_user(user_id):
        meals = Meal.query.filter_by(user_id=user_id).all()
        
        if not meals:
             return jsonify({'message': 'Nenhuma refeição encontrada para este usuário.'}), 404
    
        meals_list = []
    
        for meal in meals:
            meals_list.append({
            'id': meal.id,
            'name': meal.name,
            'description': meal.description,
            'calories': meal.calories,
            'when_at': meal.when_at,
            'in_diet': meal.in_diet,
            'created_at': meal.created_at,
            'updated_at': meal.updated_at
        })
    
        return jsonify(meals_list), 200