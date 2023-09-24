import openai
import json

# Chargez le fichier JSON local
with open("C:\\Users\\7john\\OneDrive\\Documents\\stage\\backend\\IAGORA-API\\data\\donnerExperts.json", "r") as file:
    developers = json.load(file)
    json_data = json.dumps(developers)
# Appeler l'API GPT
response = openai.Completion.create(
    engine='text-davinci-003',
    prompt = f"""{json_data}\n\nRecherche des développeurs angular avec plus de 3 ans d'expérience :""",
    max_tokens= 10000
)

# Traiter la réponse
answer = response.choices[0].text.strip()

# Afficher la réponse
print(answer)