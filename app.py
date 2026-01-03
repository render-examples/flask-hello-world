from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title>SHIELD PROTOCOL</title>
        </head>
        <body style="background-color: #0b0e11; color: #ffd700; text-align: center; font-family: sans-serif; padding-top: 100px;">
            <div style="border: 2px solid #ffd700; display: inline-block; padding: 40px; border-radius: 20px; background: rgba(0,0,0,0.8);">
                <h1 style="letter-spacing: 5px;">SHIELD PROTOCOL</h1>
                <div style="color: #00ff00; font-weight: bold; margin: 20px 0;">● SYSTÈME ACTIF ET OPÉRATIONNEL</div>
                <p style="color: white;">Votre stock Shopify est désormais sous haute protection.</p>
                <button style="background: #ffd700; color: black; border: none; padding: 15px 30px; border-radius: 50px; font-weight: bold; cursor: pointer; margin-top: 20px;">ACTIVER L'OMNISCIENCE</button>
            </div>
        </body>
    </html>
    '''
