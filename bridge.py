import paho.mqtt.client as mqtt
import json
from upstash_redis import Redis

# Configurações Upstash
# Use a URL base (Endpoint) do seu console
redis = Redis(
    url="https://neat-mackerel-90223.upstash.io", 
    token="SgQAAAAAAAWBvAAIncDIwOWZiYjEwMzIwZDE0OWRmYTI3ZjU2YjkzNDllNjlkZHAyOTAyMjM" 
)

# Configurações MQTT
MQTT_BROKER = "broker.hivemq.com"
TOPIC_REAL = "xx/inventario/peso_real"
TOPIC_VAR = "xx/inventario/variacao"

def on_connect(client, userdata, flags, rc):
    print(f"✅ Ponte Conectada ao Broker (Código {rc})")
    client.subscribe([(TOPIC_REAL, 0), (TOPIC_VAR, 0)])

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        
        if topic == TOPIC_REAL:
            # Salva o peso atual no Redis para o Dashboard de estoque
            redis.set("shelf_01:peso_atual", payload["peso"])
            print(f"📦 Estoque Atualizado: {payload['peso']}g")
            
        elif topic == TOPIC_VAR:
            # Salva o log de variações (quem tirou o quê)
            redis.lpush("shelf_01:log_eventos", json.dumps(payload))
            print(f"⚠️ Variação Detectada: {payload['variacao']}g")
            
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("🚀 Iniciando Ponte Upstash... Aguardando dados da balança.")
client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()