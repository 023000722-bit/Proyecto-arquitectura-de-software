from dataclasses import dataclass
from datetime import datetime


@dataclass
class Binary:
    id: str
    filename: str
    enviroment: str  # dev o prod
    status: str  # pending, approved, signed, rejected
    uploaded_date: datetime
    signed_path: str = None
    signature: str = None
    
    