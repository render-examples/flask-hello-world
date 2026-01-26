"""
App simplificado para Render - WhatsApp Bot
"""
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor rodando! Webhook em /webhook/whatsapp", 200

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Webhook ultra simples - responde com mensagem de sucesso"""
    
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    print(f"\n✅ MENSAGEM RECEBIDA!")
    print(f"   De: {from_number}")
    print(f"   Texto: {incoming_msg}")
    
    # Responder
    resp = MessagingResponse()
    resp.message("✅ FUNCIONOU! O webhook está ativo! 🎉")
    
    print("✅ RESPOSTA ENVIADA!\n")
    
    return str(resp), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**4️⃣ Salvar (Commit):**
- Escrever mensagem: "Update app.py for WhatsApp bot"
- Clicar "Commit changes"

**5️⃣ Editar requirements.txt:**
- Abrir `requirements.txt`
- Clicar em editar
- **APAGAR tudo**
- **COLAR:**
```
flask==3.0.0
twilio==8.10.0
gunicorn==21.2.0
```
- Commit changes

**6️⃣ Reconectar no Render:**
- Voltar para Render
- No seu serviço, ir em "Settings"
- Em "Build & Deploy" → "Git Repository"
- Mudar para SEU fork
- Clicar "Save"
- Clicar "Manual Deploy" → "Deploy latest commit"

---

## ⏰ AGUARDAR NOVO DEPLOY (2 min)

**Depois testar:**
```
https://whatsapp-bot-igxb.onrender.com
```

**Deve mostrar:**
```
Servidor rodando! Webhook em /webhook/whatsapp
