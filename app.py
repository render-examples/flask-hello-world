from flask import Flask, request
app = Flask(__name__)

from flask_cors import CORS

import json
import gensim
from flask import Response
from models import llm
from models import txtmodel
from models import jsonloader
from models import expfind


CORS(app)
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Charger le modèle pré-entraîné de Word2Vec en français
model = gensim.models.KeyedVectors.load_word2vec_format("models/frWac_non_lem_no_postag_no_phrase_200_skip_cut100.bin", binary=True)

# Fonction pour obtenir des synonymes d'un mot avec le modèle Word2Vec
def get_synonyms(word):
    synonyms = []
    # Vérifier si le mot est dans le vocabulaire du modèle
    if word in model.key_to_index:
        # Obtenir les 10 mots les plus similaires au mot donné
        similar_words = model.most_similar(word, topn=1000)
        # Extraire les mots des tuples (mot, similarité)
        for word, similarity in similar_words:
            synonyms.append(word)
    return synonyms

@app.route("/ask", methods=["POST"])
def ask():
    question = request.get_json()
    response = txtmodel.txtmodel.get_response(question['query'])

    # Vérifier si un synonyme de "apprendre" est présent dans la requête
    synonyms_learn = get_synonyms("apprendre") # Utiliser le mot "apprendre" en français pour utiliser le modèle Word2Vec
    query_lower = question['query'].lower()

    synonym_found = any(synonym in query_lower for synonym in synonyms_learn)

    # Imprimer "Tuteur Virtuel" et "Tuteur Réel" si un synonyme de "apprendre" est trouvé
    if synonym_found:
        print("Tuteur Virtuel")
        print("Tuteur Réel")
      
    return response

@app.route("/llm", methods=["POST"])
def llm_route():
    requete = request.get_json()
    print(requete['q1'])
    print(requete['url'])
    #text = request.json["text"]
    result = llm.Llm.callLlm(requete['q1'],requete['url'])
    resp = Response(result)
    resp.charset = "utf-8"
    return resp

@app.route("/expert",  methods=["POST"])
def loadjson():
    requete = request.get_json()
    results = expfind.ExpFind.findExp(requete['message'])
    return results
