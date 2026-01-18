import os
import ssl
import urllib3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ⭐⭐⭐ DÉSACTIVE SSL GLOBALEMENT AVANT TOUT ⭐⭐⭐
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "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")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL", "jolie.mountain@gmail.com")
BASE_URL = os.getenv("APP_URL", "https://finsim.up.railway.app")

def envoie_password_reset_email(to_email, token):
    print(f"🔄 [EMAIL] Tentative d'envoi à {to_email}")
    print(f"📧 [EMAIL] Expéditeur: {SENDGRID_FROM_EMAIL}")
    print(f"🌐 [EMAIL] URL de base: {BASE_URL}")
    print(f"🔑 [EMAIL] Token: {token[:10]}...")
    
    reset_link = f"{BASE_URL}/?token={token}&page=reset_password"
    print(f"🔗 [EMAIL] Lien: {reset_link}")
    
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject="Réinitialisation de votre mot de passe - FinSim",
        plain_text_content=(
            f"Bonjour,\n\n"
            f"Vous avez demandé à réinitialiser votre mot de passe pour FinSim.\n\n"
            f"Cliquez sur ce lien pour réinitialiser votre mot de passe :\n"
            f"{reset_link}\n\n"
            f"⚠️ Ce lien expire dans 1 heure.\n\n"
            f"Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.\n\n"
            f"Cordialement,\nL'équipe FinSim"
        )
    )

    try:
        if not SENDGRID_API_KEY:
            raise Exception("SENDGRID_API_KEY n'est pas configurée")
        
        print("📤 [EMAIL] Envoi via SendGrid...")
        print("⚠️ [EMAIL] SSL désactivé globalement pour contourner certificat auto-signé")
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"✅ [EMAIL] Email envoyé avec succès à {to_email}")
        print(f"📊 [EMAIL] Status code: {response.status_code}")
        
    except Exception as e:
        print(f"❌ [EMAIL] Erreur SendGrid: {e}")
        raise Exception(f"Erreur lors de l'envoi: {str(e)}")