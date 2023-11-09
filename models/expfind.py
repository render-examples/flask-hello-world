import openai
import os
import json

data_dir = os.path.join(os.path.dirname(__file__), "..", "data") 
class ExpFind:
    def findExp(message):
        # Chargez le fichier JSON local
        with open(os.path.join(data_dir, "donnerExperts.json"), "r") as file:
            developers = json.load(file)
            json_data = json.dumps(developers)
        # Appeler l'API GPT
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt = f"""{json_data}\n\n{message} :""",
            max_tokens= 1000
        )

        # Traiter la réponse
        answer = response.choices[0].text.strip()

        # Afficher la réponse
        print(answer)
        return answer