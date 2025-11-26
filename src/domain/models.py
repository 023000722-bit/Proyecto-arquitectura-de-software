from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class BinaryFile:
    id: str
    filename: str
    environment: str  # Antes enviroment, corregido a environment si tu código nuevo lo usa así
    status: str  
    uploaded_at: Optional[datetime] = None # Tu script JS espera uploaded_at
    signed_path: Optional[str] = None
    signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.uploaded_at:
            data['uploaded_at'] = self.uploaded_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BinaryFile':
        if isinstance(data.get('uploaded_at'), str):
            data['uploaded_at'] = datetime.fromisoformat(data['uploaded_at'])
        # Compatibilidad por si en json se guardó como 'enviroment' o 'uploaded_date'
        if 'enviroment' in data:
            data['environment'] = data.pop('enviroment')
        if 'uploaded_date' in data:
            data['uploaded_at'] = data.pop('uploaded_date')
            
        # Filtrar claves extra que no estén en el dataclass
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
            
        return cls(**filtered_data)