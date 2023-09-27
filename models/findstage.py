import openai

# data_dir = os.path.join(os.path.dirname(__file__), "..", "data") 
# class Findstage:
#     def findstage(message):
#         # Appeler l'API GPT
#         response = openai.Completion.create(
#             engine='text-davinci-003',
#             prompt = f"""{json_data}\n\n{message} :""",
#             max_tokens= 1000
#         )

#         # Traiter la réponse
#         answer = response.choices[0].text.strip()

#         # Afficher la réponse
#         print(answer)
#         return answer
    

response = openai.Completion.create(
engine='text-davinci-003',
# prompt = f"""{json_data}\n\n{message} :""",
prompt = "peux tu generer des requetes pour une base de donner par example j'ai une table stage, les collones sont id, nom, context, renumeration et avec le prompt que j'utilise utilise une requette sql. voici mon promt : je veux un stage en java remunerer et retourn seulement un script sql et la remuneration n'a pas besoin de devise seulement un montant aproximative ou existant",
max_tokens= 1000
        )

        # Traiter la réponse
answer = response.choices[0].text.strip()

        # Affiher la réponse
print(answer)