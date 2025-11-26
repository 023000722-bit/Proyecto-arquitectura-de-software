from flask import request, jsonify, render_template, current_app
from src.application.use_cases import UploadBinaryUseCase, SignBinaryUseCase, ApproveBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.email_service import EmailService
from src.domain.services import SigningService
from src.domain.models import BinaryFile

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/files', methods=['GET'])
    def list_files():
        return jsonify(JsonRepository().list_records()), 200

    @app.route('/upload', methods=['POST'])
    def upload_binary():
        file = request.files['file']
        environment = request.form.get('environment', 'dev')
        
        # Usamos el correo configurado en main.py como destino
        target_email = app.config['MAIL_USERNAME']

        use_case = UploadBinaryUseCase(
            FileRepository(), 
            JsonRepository(), 
            EmailService()
        )
        
        binary = use_case.execute(file, environment, target_email)
        return jsonify(binary.to_dict())

    @app.route("/sign", methods=["POST"])
    def sign_file():
        data = request.get_json()
        use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        result = use_case.execute(data.get("file_id"))
        if result: return jsonify(result.to_dict()), 200
        return jsonify({"error": "Error signing"}), 500

    @app.route('/clear', methods=['POST'])
    def clear_history():
        try:
            JsonRepository().delete_all()
            FileRepository().delete_all()
            return jsonify({"msg": "ok"}), 200
        except: return jsonify({"error": "err"}), 500

    # --- RUTA QUE SE ABRE DESDE EL CORREO ---
    @app.route('/approve/<file_id>', methods=['GET'])
    def approve_file(file_id):
        sign_use_case = SignBinaryUseCase(FileRepository(), JsonRepository(), SigningService())
        approve_use_case = ApproveBinaryUseCase(sign_use_case)
        
        success = approve_use_case.execute(file_id)
        
        # HTML con estilo en línea para la confirmación
        if success:
            return """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: linear-gradient(to right, #0f0c29, #302b63, #24243e);
                        height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0;
                        color: white;
                    }
                    .card {
                        background: rgba(255, 255, 255, 0.1);
                        backdrop-filter: blur(10px);
                        padding: 40px;
                        border-radius: 20px;
                        text-align: center;
                        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                        border: 1px solid rgba(255, 255, 255, 0.18);
                        max-width: 400px;
                        animation: popIn 0.5s ease;
                    }
                    @keyframes popIn {
                        from { transform: scale(0.8); opacity: 0; }
                        to { transform: scale(1); opacity: 1; }
                    }
                    h1 { color: #00b09b; margin-bottom: 10px; }
                    p { color: #d1d1d1; margin-bottom: 20px; }
                    .btn {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-decoration: none;
                        padding: 10px 20px;
                        border-radius: 25px;
                        font-weight: bold;
                        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1 style="font-size: 3rem;">✅</h1>
                    <h1>¡Archivo Firmado!</h1>
                    <p>El documento ha sido aprobado y procesado correctamente en el servidor.</p>
                    <br>
                    <a href="javascript:window.close()" class="btn">Cerrar Ventana</a>
                </div>
            </body>
            </html>
            """
        else:
            return """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <style>
                    body {
                        font-family: 'Segoe UI', sans-serif;
                        background: #0f0c29;
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .card {
                        background: rgba(255,255,255,0.05);
                        padding: 40px;
                        border-radius: 15px;
                        text-align: center;
                        border: 1px solid #ff416c;
                    }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1 style="color: #ff416c;">❌ Error</h1>
                    <p>El archivo no existe o ya fue firmado anteriormente.</p>
                </div>
            </body>
            </html>
            """        