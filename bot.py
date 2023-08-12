from flask import Flask, request
import openai

app = Flask(__name__)

# Clé d'accès API OpenAI
openai.api_key = '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'

# Clés d'accès Messenger
PAGE_ACCESS_TOKEN = 'EAARgJ3oIAXgBOzL8TDPUz9ONGg69tpFfi2i3HUt5zTlZBZCiqRC4gRFRGmHGZCTUxEXitIHua6qLABTAsnrosOaOIbN0hHbuBXw4wjKZCU5Df1fDZBgeqHKBAx7scvX8jUdgq3LKaMOibcJ5ZCOZBNZCVqwiBSinfTp5H5Cn4ExcdhttDkS5YxkEz3bbvvIH'
VERIFY_TOKEN = 'Ambato'

# Fonction pour obtenir une réponse de OpenAI
def conversation_openai(prompt):
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Fonction pour envoyer un message via Messenger
def send_message(recipient_id, message_text):
    import requests

    endpoint = 'https://graph.facebook.com/v12.0/me/messages'
    
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    data = {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'text': message_text
        }
    }

    response = requests.post(endpoint, params=params, json=data)
    if response.status_code == 200:
        print("Message envoyé avec succès")
    else:
        print("Échec de l'envoi du message")

# Route pour vérifier le Webhook
@app.route('/', methods=['GET'])
def verify_webhook():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Invalid verification token", 403

# Route pour recevoir les messages
@app.route('/', methods=['POST'])
def receive_message():
    data = request.get_json()

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    response_text = conversation_openai(message_text)
                    send_message(sender_id, response_text)
    
    return "Message Received", 200

if __name__ == "__main__":
    app.run(port=3000)
