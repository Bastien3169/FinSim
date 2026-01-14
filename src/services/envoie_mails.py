import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# URL dynamique selon l'environnement
BASE_URL = os.getenv("APP_URL", "http://localhost:8501")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  
#APP_URL = os.getenv("APP_URL", "https://finsim.up.railway.app")

# Email vérifié sur SendGrid
FROM_EMAIL = os.getenv("FROM_EMAIL", "jolie.mountain@gmail.com")  # doit être vérifié sur SendGrid


def envoie_password_reset_email(to_email, token):
    print(f"🔄 [EMAIL] Tentative d'envoi à {to_email}")
    print(f"🌐 [EMAIL] URL de base: {BASE_URL}")
    print(f"🔑 [EMAIL] Token: {token[:10]}...")

    # Génération du lien
    reset_link = f"{BASE_URL}/?token={token}&page=reset_password"
    print(f"🔗 [EMAIL] Lien: {reset_link}")

    # Création du message
    subject = "Réinitialisation de votre mot de passe - FinSim"
    html_content = f"""
    <p>Bonjour,</p>
    <p>Vous avez demandé à réinitialiser votre mot de passe pour FinSim.</p>
    <p>Cliquez sur ce lien pour réinitialiser votre mot de passe :</p>
    <p><a href="{reset_link}">{reset_link}</a></p>
    <p>⚠️ Ce lien expire dans 1 heure.</p>
    <p>Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.</p>
    <p>Cordialement,<br>L'équipe FinSim</p>
    """

    try:
        print("🔌 [EMAIL] Envoi via l'API SendGrid...")
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        response = sg.send(message)
        print(f"✅ [EMAIL] Email envoyé avec succès à {to_email}, code: {response.status_code}")

    except Exception as e:
        print(f"❌ [EMAIL] Erreur SendGrid: {str(e)}")
        raise Exception(f"Erreur lors de l'envoi via SendGrid: {str(e)}")
