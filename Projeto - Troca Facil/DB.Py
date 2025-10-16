from DB import db, app
with app.app_context():
        db.create_all()
from flask import Flask, requests, jsonfy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #
db = SQLAlchemy(app)


class User(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    
  
    name = db.Column(db.String(100), nullable=False)
  
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    password = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return f"User('{self.email}', '{self.name}')"


# -----------------
# 3. ROTAS DA API: CADASTRO E LOGIN
# -----------------

# Rota para Cadastro
@app.route('/api/register', methods=['POST'])
def register():

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'message': 'Preencha todos os campos.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'E-mail já cadastrado.'}), 409 # Conflict

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(name=name, email=email, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Cadastro realizado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro ao salvar: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Preencha todos os campos.'}), 400

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        return jsonify({'message': 'Login bem-sucedido!', 'name': user.name, 'auth_token': 'FICTICIO_TOKEN_123'}), 200

    return jsonify({'message': 'E-mail ou senha incorretos.'}), 401

if __name__ == '__main__':
    app.run(debug=True)