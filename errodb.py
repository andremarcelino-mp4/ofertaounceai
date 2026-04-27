from pymongo import MongoClient

MONGO_URL = "mongodb+srv://dbOncinha:Expotech2026@cluster0.ydxsizd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URL)
db = client["Oncinha"]
col = db["ofertas_ia"]

def ajustar():
    # Mapeamento de nomes que aparecem no seu terminal para os IDs corretos
    ajustes = [
        {"filtro": "Coca-Cola", "novo_id": 4},
        {"filtro": "Guaraná", "novo_id": 5},
        {"filtro": "Leite", "novo_id": 3}
    ]

    for item in ajustes:
        # Busca por nome (ignore maiúsculas/minúsculas) e define o ID numérico
        resultado = col.update_many(
            {"produto": {"$regex": item["filtro"], "$options": "i"}},
            {"$set": {"id": item["novo_id"]}}
        )
        print(f"✅ Produto {item['filtro']}: {resultado.modified_count} documentos atualizados para ID {item['novo_id']}")

if __name__ == "__main__":
    ajustar()
    print("\n🚀 Banco de dados pronto para o Ounce Stock!")