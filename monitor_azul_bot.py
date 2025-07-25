import time
import requests
from datetime import datetime

# Configurações do monitoramento
ORIGEM = "GRU"
DESTINO = "MCO"
DATA_IDA = "2025-12-19"
DATA_VOLTA = "2026-01-03"
MAX_PONTOS = 100000
NUM_ADULTOS = 3
NUM_CRIANCAS = 1
INTERVALO_MINUTOS = 5

# Telegram
TELEGRAM_TOKEN = "8225756058:AAHZzW5dMFMBsXs6ULckAV-48g5BQ6wSkO0"
TELEGRAM_USER_ID = "1533010671"  # @rodourado

def enviar_alerta(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_USER_ID,
        "text": mensagem
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def buscar_passagens():
    print("🔍 Buscando passagens...")

    # Aqui seria o scraping ou API real da Azul
    # Simulação para teste:
    resultados_ida = [
        {"data": DATA_IDA, "pontos": 95000},
    ]
    resultados_volta = [
        {"data": DATA_VOLTA, "pontos": 88000},
    ]

    alertas = []

    for r in resultados_ida:
        if r["pontos"] <= MAX_PONTOS:
            alertas.append(f"🛫 Ida em {r['data']}: {r['pontos']:,} pontos")

    for r in resultados_volta:
        if r["pontos"] <= MAX_PONTOS:
            alertas.append(f"🛬 Volta em {r['data']}: {r['pontos']:,} pontos")

    if alertas:
        msg = "💥 Passagem encontrada!\n" + "\n".join(alertas)
        enviar_alerta(msg)
        print("✅ Alerta enviado!")
    else:
        print("✈️ Nenhuma passagem encontrada no momento.")

if _name_ == "_main_":
    enviar_alerta("🤖 Bot de monitoramento iniciado!")
    while True:
        buscar_passagens()
        time.sleep(INTERVALO_MINUTOS * 60)
