# 1. Image de base : Python slim pour réduire la taille
FROM python:3.11-slim

# 2. Répertoire de travail
WORKDIR /app

# 3. Installer dépendances système essentielles (compilateurs + Chromium)
RUN apt-get update && apt-get install -y \
    # Outils de compilation pour les dépendances Python
    gcc \
    # Bibliothèques nécessaires pour Python
    python3-dev \
    libffi-dev \
    libssl-dev \
    # Bibliothèques pour le rendu de Chromium
    chromium \
    # Pilote pour Chromium (nécessaire pour Selenium)
    chromium-driver \
    # Dépendances pour Selenium
    libx11-6 \
    # Dépendances pour le rendu de Chromium 
    libxcb1 \
    # Nettoyage des caches pour réduire la taille de l'image 
    && apt-get clean && rm -rf /var/lib/apt/lists/* 

# 4. Copier requirements.txt et installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier le code de l'application
COPY . .

# 6. Variables d'environnement chromium pour Selenium afin de le trouver
ENV CHROME_BIN=/usr/bin/chromium

# 7. Uniquement pour documentation, pas nécessaire
EXPOSE 8501

# 8. Commande de lancement
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
