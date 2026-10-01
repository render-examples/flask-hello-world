from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api')
def index():
    return jsonify({
        "servidor": "Stumble Rewald",
        "versao": "0.64",
        "discord": "https://discord.gg/sgrewald",
        "status": "online"
    })

@app.route('/api/status')
def status():
    return jsonify({
        "online": True,
        "manutencao": False,
        "versao_minima": "0.64.0"
    })

@app.route('/api/profile')
def profile():
    return jsonify({
        "nome_padrao": "StumbleRewald_",
        "moedas": 0,
        "nivel": 1
    })

@app.route('/api/user')
def user():
    return jsonify({
        "id": "rewald_user",
        "conta_criada": True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

