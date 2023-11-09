import json
from pathlib import Path

class JsonLoader:
    def loadJson(path):
        data = json.loads(Path(path).read_text())
        return data
    
    def search_in_json(data, search_string):
      results = []
      for item in data:
        if search_string in item:
          results.append(item)
      return results
    

    import json

    def chercher_dans_json(cle, chaine_json):
        try:
            # Charger le JSON depuis la chaîne
            data = json.loads(chaine_json)

            # Rechercher la clé dans le JSON
            valeur = data[cle]

            return valeur
        except (json.JSONDecodeError, KeyError):
            return None
