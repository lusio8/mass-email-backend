import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build  # Corretto: importazione di build

# Scope e file di configurazione
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET_FILE = 'client_secret.json'
CREDENTIALS_DIR = 'user_credentials'  # Directory per salvare le credenziali

def get_user_credentials(user_email):
    """Gestisce le credenziali per un utente specifico."""
    os.makedirs(CREDENTIALS_DIR, exist_ok=True)
    user_token_file = os.path.join(CREDENTIALS_DIR, f"{user_email}_token.json")
    creds = None

    # Carica le credenziali esistenti
    if os.path.exists(user_token_file):
        try:
            creds = Credentials.from_authorized_user_file(user_token_file, SCOPES)
        except (json.JSONDecodeError, ValueError):
            print(f"Credenziali non valide per {user_email}. Rinnovando...")

    # Se non ci sono credenziali valide, genera nuove credenziali
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Errore nel rinnovo delle credenziali per {user_email}: {e}")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

            # Salva le credenziali per l'utente
            with open(user_token_file, 'w') as token:
                token.write(creds.to_json())

    return creds

def get_gmail_service(user_email):
    """Ritorna il servizio Gmail per un utente specifico."""
    creds = get_user_credentials(user_email)
    return build('gmail', 'v1', credentials=creds)