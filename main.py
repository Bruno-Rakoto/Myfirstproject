import openai
import requests
from flask import Flask, request

# Configurez votre clé API OpenAI
openai.api_key = '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'

app = Flask(__name__)

# Page Access Token pour l'API Messenger
PAGE_ACCESS_TOKEN = 'EAAK8pRmQnW8BOZCNTIWFW7SLpYXUdN2ZB5B4ZALpKAsrei6ZBmRxKsYytNr5Ian22zn3vuorMMUO8RcmZBytUrhvDwjPNaA5GOAM31jS6Jgoa4e0L1a4Pt3iRI7nhqPY1YcL681IZApqZAfdkQ2C6notEbWxvPCchZA0mRmwVRlJucKfEOWd4f4SnH738B3I'

# Token de vérification de Facebook Messenger
VERIFY_TOKEN = 'Moramanga'

# Route pour vérifier le token lors de la configuration du webhook
@app.route('/', methods=['GET'])
def verify_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Invalid verification token", 403

# Route pour gérer les messages entrants
@app.route('/', methods=['POST'])
def receive_message():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    
                    if message_text.lower() == 'exit':
                        send_message(sender_id, 'Discussion terminée.')
                    else:
                        ai_response = get_ai_response(message_text)
                        send_message(sender_id, ai_response)

    return "Ok", 200

def send_message(recipient_id, message_text):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post("https://graph.facebook.com/v13.0/me/messages", params=params, json=data)
    if response.status_code != 200:
        print("Erreur lors de l'envoi du message à Messenger.")

def get_ai_response(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=4000
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return 'Une erreur s\'est produite : ' + str(e)

if __name__ == '__main__':
    app.run(port=3000)
