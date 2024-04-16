import requests
import setting
import json

def get_message_whatsapp(message):
  if 'type' not in message:
    text = 'unrecognized message'
  
  typeMessage = message['type']
  if typeMessage == 'text': 
    text = message['text']['body']
    
  return text

def send_message_whatsapp(data):
  try:
    whatsapp_token = setting.WHATSAPP_TOKEN
    whatsapp_url = setting.WHATSAPP_URL
    headers = {'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + whatsapp_token}
    response = requests.post(whatsapp_url, 
                            headers=headers, 
                            data=data)
    print("se envia ", data)
    
    if response.status_code == 200:
      return 'message sent', 200
    else:
      return 'error sending message', response.status_code
  
  except Exception as e:
    return e, 403
  
def text_message(number, text):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "text",
      "text": {
          "body": text
      }
    }
  )
  
  return data

def manage_chatbot(text, number, messageId, name): 
  text = text.lower() # mensaje que recibe el usuario
  list = []
  
  data = text_message(number, "Hello test flask chatbot")
  send_message_whatsapp(data)