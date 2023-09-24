import openai
import json


# Chargez le fichier JSON local
with open("C:\\Users\\7john\\OneDrive\\Documents\stage\\backend\\IAGORA-API\\data\\donnerExperts.json", "r") as file:
    developers = json.load(file)

# Convertissez les données en une chaîne JSON
json_data = json.dumps(developers)

# Définissez le prompt avec la chaîne JSON
prompt = f"""{json_data}\n\nRecherche des développeurs java avec plus de 3 ans d'expérience :"""

# Demandez à GPT-3 de filtrer les développeurs
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=1000
)

# Analysez la réponse pour extraire les développeurs filtrés
filtered_developers = []
data = response.choices[0].text.strip().split('\n')
for entry in data:
    expert = eval(entry)
    if expert["specialization"] == "Java" and expert["years_of_experience"] > 3:
        filtered_developers.append(expert)

print(filtered_developers)
