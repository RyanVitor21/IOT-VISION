import requests

# 🔑 Configure seu token e device
UBIDOTS_TOKEN = "BBUS-LYbWdeRmn4ZvHbILBPbWB5REjmcDid"
DEVICE_LABEL = "vision-iot"  # nome do dispositivo no Ubidots
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/?forceCreate=true"

def send_to_ubidots(total, inside, outside):
    """
    Envia os dados de contagem para o Ubidots.
    Se as variáveis não existirem, elas serão criadas automaticamente.
    """
    payload = {
        "total_count": total,
        "inside_count": inside,
        "outside_count": outside,
    }

    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(UBIDOTS_URL, json=payload, headers=headers, timeout=5)
        if response.status_code in [200, 201]:
            print(f"📡 Dados enviados para Ubidots: {payload}")
        else:
            print(f"⚠️ Erro ao enviar dados: {response.status_code} -> {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão com Ubidots: {e}")



        
#Entre no Ubidots Vá em Devices > Your Device (o dispositivo que você criou).

#Lá dentro, crie manualmente 3 variáveis com esses nomes:  outside_count total_count Depois rode o detector.py de novo → agora os valores vão ser aceitos.
#


