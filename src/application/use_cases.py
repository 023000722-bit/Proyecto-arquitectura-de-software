from datetime import datetime
from uuid import uuid4
from typing import Optional
from src.domain.models import BinaryFile
from src.domain.services import SigningService

class UploadBinaryUseCase:
    def __init__(self, file_repo, db_repo, email_service=None):
        self.file_repo = file_repo
        self.db_repo = db_repo
        self.email_service = email_service
        
    def execute(self, file, environment: str, user_email: str = None) -> BinaryFile:
        binary_id = str(uuid4())
        filename = self.file_repo.save(file, binary_id)
        
        # Prod = pending (esperando correo), Dev = pending (listo para firmar manual)
        status = 'pending'
        
        binary = BinaryFile(
            id=binary_id,
            filename=filename,
            environment=environment,
            status=status,
            uploaded_at=datetime.now()
        )
        
        self.db_repo.add_record(binary.to_dict())
        
        # LOGICA DE PRODUCCIÓN: Enviar correo
        if environment == 'prod' and self.email_service and user_email:
            self.email_service.send_approval_email(user_email, binary.id, binary.filename)
            
        return binary

class SignBinaryUseCase:
    def __init__(self, file_repo, json_repo, signing_service):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service
            
    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.json_repo.get_record(file_id)
        if not record: return None
        
        try:
            # Convertir a objeto
            binary = BinaryFile.from_dict(record)
            
            # Firmar
            signature, signed_path = self.signing_service.sign_file(binary)

            # Actualizar estado
            binary.status = "signed"
            binary.signed_path = signed_path
            binary.signature = signature
            
            # Guardar cambios
            self.json_repo.update_record(binary.id, binary.to_dict())
            return binary
            
        except Exception as e:
            print(f"Error firmando: {e}")
            return None

class ApproveBinaryUseCase:
    def __init__(self, sign_use_case):
        self.sign_use_case = sign_use_case

    def execute(self, file_id: str) -> bool:
        # Al aprobar, simplemente ejecutamos la firma
        result = self.sign_use_case.execute(file_id)
        return result is not None