# Image de base officielle Python
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier l'application et le dossier utils
COPY app.py .
COPY utils /app/utils  

# Exposer le port
EXPOSE 8080

# Commande pour lancer l'application
CMD ["python", "app.py"]
