# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Настройки базы данных PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

# Создание базы данных
with app.app_context():
    db.create_all()

# Маршрут для получения списка пицц
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{'id': pizza.id, 'name': pizza.name, 'description': pizza.description, 'price': pizza.price, 'image_url': pizza.image_url} for pizza in pizzas])

# Маршрут для добавления новой пиццы
@app.route('/pizzas', methods=['POST'])
def add_pizza():
    data = request.json
    new_pizza = Pizza(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data.get('image_url')
    )
    db.session.add(new_pizza)
    db.session.commit()
    return jsonify({'message': 'Pizza added successfully!'}), 201

# Маршрут для обновления существующей пиццы
@app.route('/pizzas/<int:pizza_id>', methods=['PUT'])
def update_pizza(pizza_id):
    data = request.json
    pizza = Pizza.query.get(pizza_id)
    if not pizza:
        return jsonify({'message': 'Pizza not found'}), 404

    pizza.name = data['name']
    pizza.description = data['description']
    pizza.price = data['price']
    pizza.image_url = data.get('image_url')

    db.session.commit()
    return jsonify({'message': 'Pizza updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
