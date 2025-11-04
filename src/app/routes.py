from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/upload', methods=['POST'])
    def upload_binary():
        # Get file and environment from form data
        file = request.files['file']
        environment = request.form.get('environment', 'dev')
        
        #Ivoque "upload binary use case with current context
        use_case = UploadBinaryUseCase(FileRepository(),JsonRepository())
        binary = use_case.execute(file, environment)
        
        #return Json response with binary metadata
        return jsonify({
            'id': binary.id,
            'status': binary.status,
        })
             
