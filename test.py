from pymongo import MongoClient

# Sua conexão
MONGO_URL = "mongodb+srv://dbOncinha:Expotech2026@cluster0.ydxsizd.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)
db = client["Oncinha"]
col = db["ofertas_ia"]

print("\n--- TESTE DE DADOS OUNCE STOCK ---")
produtos = col.find()

for p in produtos:
    p_id = p.get("produto_id")
    nome = p.get("nome", "Sem nome")
    frases = p.get("frases", [])
    print(f"ID: {p_id} | Produto: {nome} | Frases: {frases}")

print("----------------------------------\n")