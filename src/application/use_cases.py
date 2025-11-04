from datetime import datetime
from uuid import uuid4
from src.domain.models import Binary

class UploadBinaryUseCase:
    def __init__(self, file_repo, db_repo):
        self.file_repo = file_repo
        self.db_repo = db_repo
        
    def execute(self, file, enviroment: str) -> Binary:
        binary_id = str(uuid4())
        filename = self.file_repo.save_file(file, binary_id)
        binary = Binary(
            id =binary_id,
            filename=filename,
            enviroment=enviroment,
            status='pending' if enviroment == 'prod' else 'signed',
            uploaded_date=datetime.now()
        )
        self.db_repo.add(binary)
        return binary
        return binary