from flask import Flask, request
import setting
import services

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def hello_world():
    return '<p>Hello, Worldsssds!</p>'

@app.route('/welcome', methods=['GET'])
def welcome():
    return '<p>Bienvenido!</p>'

@app.route('/webhook', methods=['GET'])
def verify_token():
    try:
        token = request.args.get('hub.verify_foken')
        challenge = request.args.get('hub.challenge')
    except Exception as e:
        return e,403
    
    if token == setting.TOKEN and challenge != None:
        return challenge,200
    else:
        return 'Invalid token',403

@app.route('/webhook', methods=['POST'])
def recive_message():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['message'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.get_message_whatsapp(message)
        
        services.manage_chatbot(text, number, messageId, name)
        return 'Message sent'
    
    except Exception as e:
        return 'Unsent message'

if __name__ == '__main__':
    app.run()