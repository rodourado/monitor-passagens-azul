import requests
import time
from datetime import datetime
import os
import logging

# --- CONFIGURAÇÕES DO BOT ---
TOKEN_TELEGRAM = "8225756058:AAHZzW5dMFMBsXs6ULckAV-48g5BQ6wSkO0"
USERNAME_TELEGRAM = "rodourado"  # sem @

# --- CONFIGURAÇÕES DE BUSCA ---
ORIGEM = "GRU"
DESTINO = "MCO"
DATA_IDA = "2025-12-19"
DATA_VOLTA = "2026-01-03"
ADULTOS = 3
CRIANCAS = 1
PONTOS_MAXIMOS = 100_000  # por trecho
INTERVALO_MINUTOS = 5

# --- CONFIGURAÇÃO DE LOG ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def buscar_passagens(origem, destino, data, adultos, criancas):
    url = "https://bff.voeazul.com.br/availability/availability"
    payload = {
        "adult": adultos,
        "child": criancas,
        "infant": 0,
        "cabin": "all",
        "origin": origem,
        "destination": destino,
        "outboundDate": data,
        "currency": "points",
        "tripType": "oneWay",
        "channel": "WEB",
        "searchType": "fare",
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Erro na busca: {e}")
        return None


def menor_valor(resposta_json):
    if not resposta_json:
        return None
    try:
        fares = resposta_json["outbound"]["availability"]
        pontos = [f["price"]["amount"] for f in fares if f["price"]["currency"] == "points"]
        return min(pontos) if pontos else None
    except Exception as e:
        logging.error(f"Erro ao extrair valor: {e}")
        return None


def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        "chat_id": f"@{USERNAME_TELEGRAM}",
        "text": mensagem,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, json=payload)
        if r.status_code != 200:
            logging.warning(f"Erro ao enviar mensagem: {r.text}")
    except Exception as e:
        logging.error(f"Erro Telegram: {e}")


def formatar_msg(pontos_ida, pontos_volta):
    total = pontos_ida + pontos_volta
    return f"""
💥 <b>Passagem encontrada!</b>

🛫 Origem: {ORIGEM}
🛬 Destino: {DESTINO}
📅 Ida: {DATA_IDA} | Volta: {DATA_VOLTA}
👨‍👩‍👧 Passageiros: {ADULTOS} adultos + {CRIANCAS} criança(s)

🔢 Pontos ida: {pontos_ida:,}
🔢 Pontos volta: {pontos_volta:,}

💸 <b>Total: {total:,} pontos</b>
"""


def monitorar():
    while True:
        logging.info("Buscando passagens...")

        ida = buscar_passagens(ORIGEM, DESTINO, DATA_IDA, ADULTOS, CRIANCAS)
        volta = buscar_passagens(DESTINO, ORIGEM, DATA_VOLTA, ADULTOS, CRIANCAS)

        pontos_ida = menor_valor(ida)
        pontos_volta = menor_valor(volta)

        if pontos_ida and pontos_volta:
            if pontos_ida <= PONTOS_MAXIMOS and pontos_volta <= PONTOS_MAXIMOS:
                msg = formatar_msg(pontos_ida, pontos_volta)
                enviar_telegram(msg)

        logging.info("Aguardando próxima verificação...")
        time.sleep(INTERVALO_MINUTOS * 60)


if _name_ == "_main_":
    monitorar()
