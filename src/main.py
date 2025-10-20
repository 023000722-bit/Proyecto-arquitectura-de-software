# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: main.py
# Descripción: Archivo principal del proyecto.
# ============================================================
from cryptography.fernet import Fernet

# Put this somewhere safe!
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"A really secret message. Not for prying eyes.")
print(f"Token generated:", type(token))
print(token)
print(f.decrypt(token))