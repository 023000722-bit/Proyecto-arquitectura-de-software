import sys
import os
from pathlib import Path

# Ajuste de rutas
sys.path.append(str(Path(__file__).parent.parent.parent))

from flask import Flask
from flask_mail import Mail
from src.app.routes import register_routes
from src.common.vars import HOME_HOST

def create_app():
    app = Flask(__name__, template_folder='templates')

    # --- CONFIGURACIÓN DEL CORREO (GMAIL) ---
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    
 
    
    app.config['MAIL_USERNAME'] = 'maffs1124@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'hamx wthz pwdq clbk' 
    


    app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

    # Inicializar Flask-Mail
    app.mail = Mail(app)

    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=HOME_HOST, debug=True)