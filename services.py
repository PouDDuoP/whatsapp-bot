import requests
import setting
import json
import time

def get_message_whatsapp(message):
  if 'type' not in message:
    text = 'unrecognized message'
    return text
  
  typeMessage = message['type']
  if typeMessage == 'text': 
    text = message['text']['body']
  elif typeMessage == 'button': 
    text = message['button']['text']
  elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply': 
    text = message['interactive']['list_reply']['title']
  elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply': 
    text = message['interactive']['button_reply']['title']
  else:
    text = 'menbsaje no reconocido'
    
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

def button_reply_message(number, options, body, footer, sedd, messageId):
  buttons = []
  for i, option in enumerate(options):
    buttons.append(
      {
        "type": "reply",
        "reply": {
          "id": sedd + "_btn_" + str(i+1),
          "title": option
        }
      }
    )
    
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "interactive",
      "interactive": {
        "type": "button",
        "body": {
          "text": body
        },
        "footer": {
          "text": footer
        },
        "action": {
          "buttons": buttons
        }
      }
    }
  )
  return data

def list_reply_message(number, options, body, footer, sedd, messageId):
  rows = []
  for i, option in enumerate(options):
    rows.append(
      {
        "id": sedd + "_btn_" + str(i+1),
        "title": option,
        "description": ""
      }
    )
    
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "interactive",
      "interactive": {
        "type": "list",
        "body": {
          "text": body
        },
        "footer": {
          "text": footer
        },
        "action": {
          "button": "Ver Opciones",
          "sections": [
            {
              "title": "Secciones",
              "rows": rows
            }
          ]
        }
      }
  }
  )
  return data

def document_message(number, url, caption, filename):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "document",
      "document": {
        "url": url,
        "caption": caption,
        "filename": filename
      }
    }
  )
  return data

def sticker_message(number, stickerId):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "sticker",
      "sticker": {
        "id": stickerId
      }
    }
  )
  
def get_media_id(mediaName, mediaType):
  mediaId = ""
  
  if mediaType == "sticker":
    mediaId = setting.STICKERS.get(mediaName, None)
  # elif mediaType == "image":
  #   mediaId = setting.IMAGES.get(mediaName, None)
  # elif mediaType == "video":
  #   mediaId = setting.VIDEOS.get(mediaName, None)
  # elif mediaType == "audio":
  #   mediaId = setting.AUDIOS.get(mediaName, None)
  return mediaId

def reply_reaction_message(number, messageId, emoji):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "type": "reaction",
      "reaction": {
        "message_id": messageId,
        "emoji": emoji
      }
    }
  )
  return data

def reply_text_message(number, messageId, text):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "recipient_type": "individual",
      "to": number,
      "context": { "message_id": messageId },
      "type": "text",
      "text": {
        "body": text
      }
    }
  )
  return data

def mark_read_message(messageId):
  data = json.dumps(
    {
      "messaging_product": "whatsapp",
      "status": "read",
      "message_id": messageId
    }
  )
  return data

def manage_chatbot(text, number, messageId, name): 
  text = text.lower() # mensaje que recibe el usuario
  list = []
  
  print("texto recibido: ",text)
  
  markRead = mark_read_message(messageId)
  list.append(markRead)
  time.sleep(2)
  
  if "hola" in text:
    body = "Hola! esto es una prueba de ChatBot!"
    footer = "Footer ChatBot KAAG"
    options = ["✅ Ver Servicios", "📅 Disponibilidad!"]
    
    replyButtonData = button_reply_message(number, options, body, footer, "sed1", messageId)
    replyReaction = reply_reaction_message(number, messageId, "👋")
    
    list.append(replyReaction)
    list.append(replyButtonData)
  
  elif "ver servicios" in text:
    body = "Servicios disponibles:"
    footer = "Footer ChatBot KAAG"
    options = ["Carta aval", "Asistencia de viaje", "Cotizacion de poliza"]
    
    listReplyData = list_reply_message(number, options, body, footer, "sed2", messageId)
    sticker = sticker_message(number, get_media_id('poyo_feliz', "sticker"))
    
    list.append(listReplyData)
    list.append(sticker)
    
  elif "cotizacion de poliza" in text:
    body = "Desea recibir un pdf con la cotizacion?"
    footer = "Footer ChatBot KAAG"
    options = ["✅ Si, envia el PDF.", "⛔ No, gracias"]

    replyButtonData = button_reply_message(number, options, body, footer, "sed3", messageId)
    list.append(replyButtonData)
    
  elif "si, envía el pdf" in text:
    sticker = sticker_message(number, get_media_id("pelfet", "sticker"))
    textMessage = text_message(number, "Por favor espera un momento.")

    send_message_whatsapp(sticker)
    send_message_whatsapp(textMessage)
    time.sleep(3)

    document = document_message(number, setting.DOCUMENT_URL, "Listo 👍🏻", "cotizacion.pdf")
    send_message_whatsapp(document)
    time.sleep(3)

    body = "¿Desa una cita con algun ejecutivo para proseguir con la cotizacion?"
    footer = "Footer ChatBot KAAG"
    options = ["✅ Sí, agenda reunion", "No, gracias." ]

    replyButtonData = button_reply_message(number, options, body, footer, "sed4", messageId)
    list.append(replyButtonData)
    
  elif "si, agenda reunion" in text :
      body = "Estupendo. Por favor indique una hora para la reunión:"
      footer = "Footer ChatBot KAAG"
      options = ["📅 Mañana a las 10:00 AM", "📅 Mañana a las 2:00 PM", "📅 Mañana a las 4:00 PM"]

      listReply = list_reply_message(number, options, body, footer, "sed5", messageId)
      list.append(listReply)
      
  elif "mañana a las 2:00 pm" in text:
      body = "Se ha programado una reunion para las 2:00 PM. ¿Necesitas ayuda con algo más hoy?"
      footer = "Footer ChatBot KAAG"
      options = ["✅ Sí, por favor", "❌ No, gracias."]


      buttonReply = button_reply_message(number, options, body, footer, "sed6", messageId)
      list.append(buttonReply)
      
  elif "no, gracias." in text:
      textMessage = text_message(number, "Perfecto! No dudes en contactarnos si tienes más preguntas. Recuerda que también ofrecemos material gratuito para la comunidad. ¡Hasta luego! 😊")
      list.append(textMessage)
  else :
      data = text_message(number, "Lo siento, no entendí lo que dijiste. ¿Quieres que te ayude con alguna de estas opciones?")
      list.append(data)
      
      body = "Servicios disponibles:"
      footer = "Footer ChatBot KAAG"
      options = ["Carta aval", "Asistencia de viaje", "Cotizacion de poliza"]
      
      listReplyData = list_reply_message(number, options, body, footer, "sed2", messageId)
      sticker = sticker_message(number, get_media_id('poyo_feliz', "sticker"))
      
      list.append(listReplyData)
      list.append(sticker)

  for item in list:
      send_message_whatsapp(item)
  
  # data = text_message(number, "Hello test flask chatbot")
  # send_message_whatsapp(data)