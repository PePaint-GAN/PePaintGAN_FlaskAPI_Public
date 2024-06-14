import datetime
import uuid
from flask import Blueprint, jsonify, request
from database.db import initialize_firestore_and_storage
from components.newimage import generate_images
import os
from firebase_admin import storage

# Creo un Blueprint para las rutas de la API
painting_blueprint = Blueprint('painting', __name__)

# Obtengo una instancia de la base de datos de Firestore
db = initialize_firestore_and_storage()

@painting_blueprint.route('/list', methods=['GET'])
def getPaintings():
    try:
        painting_ref = db.collection('painting')
        painting = [doc.to_dict() for doc in painting_ref.stream()]
        return jsonify(painting), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@painting_blueprint.route('/add', methods=['POST'])
def createPainting():
    try:
        painting_ref = db.collection('painting')
        id = uuid.uuid4().hex
        painting_ref.document(id).set(request.get_json())
        painting_ref.document(id).update({'id': id})
        return jsonify({'message': 'Painting created'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@painting_blueprint.route('/update/<id>', methods=['PUT'])
def updatePainting(id):
    try:
        painting_ref = db.collection('painting').document(id)
        painting_ref.update(request.get_json())
        return jsonify({'message': 'Painting updated'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@painting_blueprint.route('/delete/<id>', methods=['DELETE'])
def deletePainting(id):
    try:
        painting_ref = db.collection('painting').document(id)
        painting_ref.delete()
        return jsonify({'message': 'Painting deleted'}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@painting_blueprint.route('/get/<id>', methods=['GET'])
def getPainting(id):
    try:
        painting_ref = db.collection('painting').document(id)
        painting = painting_ref.get()
        return jsonify(painting.to_dict()), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@painting_blueprint.route('/list/<user_id>', methods=['GET'])
def getPaintingsByUserId(user_id):
    try:
        painting_ref = db.collection('painting')
        # Filtra las pinturas por user_id
        paintings = [doc.to_dict() for doc in painting_ref.where('user_id', '==', user_id).stream()]
        return jsonify(paintings), 200
    except Exception as e:
        return f"An Error Occurred: {e}"
    

@painting_blueprint.route('/generate_images/<model_name>', methods=['POST'])
def generateAndSaveImages(model_name):
    try:
        num_images = request.json.get('numImages')

        # Llama a la función generate_images para generar las imágenes
        output_folder = './images'
        model_checkpoint = f'./model/{model_name}.pth'
        generate_images(output_folder, model_checkpoint, int(num_images))

        # Accede a Firebase Cloud Storage
        bucket = storage.bucket()

        # Lista para almacenar las URLs de las imágenes en Firebase Cloud Storage
        image_urls = []

        # Recorre las imágenes generadas
        for filename in os.listdir(output_folder):
            image_path = os.path.join(output_folder, filename)

            # Sube directamente la imagen a Firebase Cloud Storage
            with open(image_path, 'rb') as image_file:
                 blob = bucket.blob(f'{filename}')
                 blob.upload_from_file(image_file, content_type='image/jpeg')

            # Obtiene la URL de descarga de la imagen en Firebase Cloud 
            project_name = ''
            image_url = f"https://firebasestorage.googleapis.com/v0/b/{project_name}.appspot.com/o/{filename}?alt=media"

            # Guarda la URL en la lista
            image_urls.append(image_url)

            # Elimina la imagen generada
            os.remove(image_path)

        # Devuelve las URLs de las imágenes generadas
        return jsonify({'image_urls': image_urls}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"