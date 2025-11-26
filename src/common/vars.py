import os

# Calculamos la ruta base dinámicamente para que funcione en cualquier PC
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Definición de Directorios según el profe
ROOT_DIR = BASE_DIR
SRC_DIR = os.path.join(ROOT_DIR, "src")
DATA_DIR = os.path.join(ROOT_DIR, "data", "binaries") # Aquí se guardan los que subes
SIGNED_DIR = os.path.join(ROOT_DIR, "data", "signed") # Aquí se guardan los firmados
TEMPLATES_DIR = os.path.join(SRC_DIR, "app", "templates")

# Configuración del servidor
HOME_HOST = 8080

# Aseguramos que existan las carpetas
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(SIGNED_DIR, exist_ok=True)