# Archivo: src/infrastructure/email_service.py
from flask_mail import Message
from flask import current_app, url_for

class EmailService:
    def send_approval_email(self, recipient_email: str, file_id: str, filename: str):
        try:
            # Genera el enlace de aprobación
            approval_link = url_for('approve_file', file_id=file_id, _external=True)
            
            # Plantilla HTML para el correo
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                        <h2 style="color: #ffffff; margin: 0;">Solicitud de Firma Digital</h2>
                        <p style="color: #e0e0e0; margin-top: 5px;">Entorno de Producción</p>
                    </div>
                    <div style="padding: 30px; color: #333333;">
                        <p>Hola,</p>
                        <p>El archivo <strong>{filename}</strong> ha sido subido y requiere tu aprobación para ser firmado.</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{approval_link}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; display: inline-block;">
                                Aprobar y Firmar Documento
                            </a>
                        </div>
                        <p style="font-size: 12px; color: #999;">Si no solicitaste esta acción, puedes ignorar este correo.</p>
                    </div>
                    <div style="background-color: #eeeeee; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                        Sistema de Arquitectura de Software - 2025
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg = Message(
                subject=f"🚀 Acción Requerida: Firmar {filename}",
                recipients=[recipient_email],
                html=html_body  # Usamos 'html' en lugar de 'body'
            )
            
            current_app.mail.send(msg)
            print(f"✅ Correo enviado a {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")
            return False