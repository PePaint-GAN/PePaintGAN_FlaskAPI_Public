import uuid
from flask import Blueprint, jsonify, request
from database.db import initialize_firestore_and_storage

# Creo un Blueprint para las rutas de la API
artistContact_blueprint = Blueprint('artistContact', __name__)

# Obtengo una instancia de la base de datos de Firestore
db = initialize_firestore_and_storage()

@artistContact_blueprint.route('/list', methods=['GET'])
def getArtistContacts():
    try:
        artistContact_ref = db.collection('artistContact')
        artistContact = [doc.to_dict() for doc in artistContact_ref.stream()]
        return jsonify(artistContact), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@artistContact_blueprint.route('/add', methods=['POST'])
def createArtistContact():
    try:
        artistContact_ref = db.collection('artistContact')
        id = uuid.uuid4().hex
        artistContact_ref.document(id).set(request.get_json())
        artistContact_ref.document(id).update({'id': id})
        return jsonify({'message': 'ArtistContact created'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@artistContact_blueprint.route('/update/<id>', methods=['PUT'])
def updateArtistContact(id):
    try:
        artistContact_ref = db.collection('artistContact').document(id)
        artistContact_ref.update(request.get_json())
        return jsonify({'message': 'ArtistContact updated'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@artistContact_blueprint.route('/delete/<id>', methods=['DELETE'])
def deleteArtistContact(id):
    try:
        artistContact_ref = db.collection('artistContact').document(id)
        artistContact_ref.delete()
        return jsonify({'message': 'ArtistContact deleted'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@artistContact_blueprint.route('/get/<id>', methods=['GET'])
def getArtistContact(id):
    try:
        artistContact_ref = db.collection('artistContact').document(id)
        artistContact = artistContact_ref.get()
        return jsonify(artistContact.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"