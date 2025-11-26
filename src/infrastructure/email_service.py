
from flask_mail import Message
from flask import current_app, url_for

class EmailService:
    def send_approval_email(self, recipient_email: str, file_id: str, filename: str):
        try:
            # Genera el enlace: http://localhost:8080/approve/ID...
            approval_link = url_for('approve_file', file_id=file_id, _external=True)
            
            msg = Message(
                subject=f"Requiere Aprobación: {filename}",
                recipients=[recipient_email],
                body=f"""
                SOLICITUD DE FIRMA PARA PRODUCCIÓN
                
                El archivo '{filename}' ha sido subido y está en espera.
                
                Para aprobarlo y firmarlo digitalmente, haga clic aquí:
                {approval_link}
                
                Si usted no solicitó esto, ignore el mensaje.
                """
            )
            
            current_app.mail.send(msg)
            print(f"✅ Correo enviado a {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")
            return False