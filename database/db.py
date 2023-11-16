from firebase_admin import credentials, initialize_app, firestore

initialized = False

def initialize_firestore_and_storage():
    global initialized

    if not initialized:
        # Creo una credencial de servicio para autenticarme en Firebase
        cred = credentials.Certificate("database/key.json")
        initialize_app(cred, {
            'storageBucket': 'paintgan-a23b4.appspot.com'  # Reemplaza con el nombre de tu proyecto
        })

        initialized = True
    
    # Obtengo una instancia de la base de datos de Firestore
    return firestore.client()