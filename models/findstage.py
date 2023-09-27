import openai
import oraclecnx
import json
class Findstage:
    def findstage(message):
        # Appeler l'API GPT
        response = openai.Completion.create(
        engine='text-davinci-003',
        # prompt = f"""{json_data}\n\n{message} :""",
        prompt = f""""peux tu generer des requetes pour une base de donner par example j'ai une table stage, les collones sont id, nom, context, remuneration et avec le prompt que j'utilise utilise une requette sql. 
        voici mon promt : \n\n{message}\n\n 
        et retourne seulement un script sql et la remuneration n'a pas besoin de devise seulement un montant aproximative ou existant""",
        
        max_tokens= 1000
        )

        # Traiter la réponse
        answer = response.choices[0].text.strip()

        # Affiher la réponse
        print(answer)

        cursor = oraclecnx.cursor()
        cursor.execute(answer)
        result = cursor.fetchall()

        data_as_json = []

        for row in result:
            data_as_json.append({
            "id": row[0],
            "nom": row[1],
            "contexte": row[2],
            "remuneration": row[3]
    })

        cursor.close()
        oraclecnx.close()

        json_data = json.dumps(data_as_json, indent=4)

        return json_data
        