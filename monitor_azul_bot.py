import requests
import time
import datetime
from twilio.rest import Client

# Configurações do alerta
TWILIO_SID = "SEU_TWILIO_SID"
TWILIO_TOKEN = "SEU_TWILIO_TOKEN"
TWILIO_PHONE = "whatsapp:+14155238886"  # Número do Twilio Sandbox para WhatsApp
DESTINO = "whatsapp:+5511970771743"     # Seu número com DDI do Brasil

# Parâmetros da busca
ORIGEM = "GRU"
DESTINO_CIDADE = "MCO"
DATA_IDA = "2025-12-19"
DATA_VOLTA = "2026-01-03"
MAX_PONTOS = 100000
ADULTOS = 3
CRIANÇAS = 1

def buscar_passagens(data):
    url = "https://bff-mobileapps.flyazul.com.br/availability/api/v1/availability/search"
    payload = {
        "cabinType": "ECONOMY",
        "channel": "WEB",
        "currencyCode": "BRL",
        "itineraryAvailabilityList": [{
            "origin": ORIGEM,
            "destination": DESTINO_CIDADE,
            "departureDate": data
        }],
        "adultCount": ADULTOS,
        "childCount": CRIANÇAS,
        "infantCount": 0,
        "isFlexibleDateChecked": False,
        "loyaltyProgram": "TudoAzul",
        "tripType": "OneWay"
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "okhttp/4.9.0"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        voos = data["availabilitySearchResponseList"][0]["itineraryList"]

        for voo in voos:
            menor_valor = voo["itineraryPrices"][0]["priceDetailList"][0]["loyalty"]["points"]
            if menor_valor <= MAX_PONTOS:
                return menor_valor
    except Exception as e:
        print(f"Erro ao buscar passagens: {e}")
    return None

def enviar_whatsapp(msg):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        from_=TWILIO_PHONE,
        body=msg,
        to=DESTINO
    )
    print(f"Mensagem enviada: {message.sid}")

if __name__ == "__main__":
    while True:
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{agora}] Verificando passagens...")

        pontos_ida = buscar_passagens(DATA_IDA)
        pontos_volta = buscar_passagens(DATA_VOLTA)

        if pontos_ida and pontos_volta:
            msg = f"💥 Passagem encontrada!
Ida: {pontos_ida} pontos
Volta: {pontos_volta} pontos"
            enviar_whatsapp(msg)

        time.sleep(300)  # 5 minutos