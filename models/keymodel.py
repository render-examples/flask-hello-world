import os

class KeyModel:
    def load_openai_api_key():
        # Charge le fichier .env
        with open(".env", "r") as f:
            env = f.read()

        # Récupère la clé API OpenAI
        return os.environ.get("OPENAI_API_KEY", "")
