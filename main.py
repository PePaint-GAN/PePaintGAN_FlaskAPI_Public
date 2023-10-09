from flask import Flask
from flask_cors import CORS
from cruds.userCRUD import user_blueprint
from cruds.artistContactCRUD import artistContact_blueprint
from cruds.styleCRUD import style_blueprint
from cruds.paintingCRUD import painting_blueprint
from database.db import initialize_firestore_and_storage

app = Flask(__name__)

# Configurar CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Obtengo una instancia de la base de datos de Firestore
initialize_firestore_and_storage()

# Registro de Blueprints
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(artistContact_blueprint, url_prefix='/api/artistContact')
app.register_blueprint(style_blueprint, url_prefix='/api/style')
app.register_blueprint(painting_blueprint, url_prefix='/api/painting')

if __name__ == '__main__':
    app.run(debug=True)