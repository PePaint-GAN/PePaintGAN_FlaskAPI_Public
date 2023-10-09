import uuid
from flask import Blueprint, jsonify, request
from database.db import initialize_firestore_and_storage

# Creo un Blueprint para las rutas de la API
style_blueprint = Blueprint('style', __name__)

# Obtengo una instancia de la base de datos de Firestore
db = initialize_firestore_and_storage()

@style_blueprint.route('/list', methods=['GET'])
def getStyles():
    try:
        style_ref = db.collection('c')
        style = [doc.to_dict() for doc in style_ref.stream()]
        return jsonify(style), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@style_blueprint.route('/add', methods=['POST'])
def createStyle():
    try:
        style_ref = db.collection('style')
        id = uuid.uuid4().hex
        style_ref.document(id).set(request.get_json())
        style_ref.document(id).update({'id': id})
        return jsonify({'message': 'Style created'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@style_blueprint.route('/update/<id>', methods=['PUT'])
def updateStyle(id):
    try:
        style_ref = db.collection('style').document(id)
        style_ref.update(request.get_json())
        return jsonify({'message': 'Style updated'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@style_blueprint.route('/delete/<id>', methods=['DELETE'])
def deleteStyle(id):
    try:
        style_ref = db.collection('style').document(id)
        style_ref.delete()
        return jsonify({'message': 'Style deleted'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@style_blueprint.route('/get/<id>', methods=['GET'])
def getStyle(id):
    try:
        style_ref = db.collection('style').document(id)
        style = style_ref.get()
        return jsonify(style.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"