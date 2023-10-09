import uuid
from flask import Blueprint, jsonify, request
from database.db import initialize_firestore_and_storage

# Creo un Blueprint para las rutas de la API
user_blueprint = Blueprint('user', __name__)

# Obtengo una instancia de la base de datos de Firestore
db = initialize_firestore_and_storage()

@user_blueprint.route('/list', methods=['GET'])
def getUsers():
    try:
        user_ref = db.collection('user')
        user = [doc.to_dict() for doc in user_ref.stream()]
        return jsonify(user), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@user_blueprint.route('/add', methods=['POST'])
def createUser():
    try:
        user_ref = db.collection('user')
        user_ref.document(request.get_json()["id"]).set(request.get_json())
        return jsonify({'message': 'User created'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@user_blueprint.route('/update/<id>', methods=['PUT'])
def updateUser(id):
    try:
        user_ref = db.collection('user').document(id)
        user_ref.update(request.get_json())
        return jsonify({'message': 'User updated'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@user_blueprint.route('/delete/<id>', methods=['DELETE'])
def deleteUser(id):
    try:
        user_ref = db.collection('user').document(id)
        user_ref.delete()
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@user_blueprint.route('/get/<id>', methods=['GET'])
def getUser(id):
    try:
        user_ref = db.collection('user').document(id)
        user = user_ref.get()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"