import smtplib
from email.message import EmailMessage

# ---- Variables simples pour test ----
SMTP_EMAIL = "jolie.mountain@gmail.com"
SMTP_PASS = "oxwp quqm exbt bgjx"  # mot de passe spécifique application
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def envoie_password_reset_email(to_email, token):
    # ⭐ Utiliser le bon port de votre app Streamlit
    reset_link = f"http://localhost:8501/?token={token}&page=reset_password"
    
    msg = EmailMessage()
    msg['Subject'] = "Réinitialisation de votre mot de passe - FinSim"
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    
    msg.set_content(
        f"Bonjour,\n\n"
        f"Vous avez demandé à réinitialiser votre mot de passe pour FinSim.\n\n"
        f"Cliquez sur ce lien pour réinitialiser votre mot de passe :\n"
        f"{reset_link}\n\n"
        f"⚠️ Ce lien expire dans 1 heure.\n\n"
        f"Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.\n\n"
        f"Cordialement,\nL'équipe FinSim"
    )

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(SMTP_EMAIL, SMTP_PASS)
        smtp.send_message(msg)