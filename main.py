from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão Ounce Stock
MONGO_URL = "mongodb+srv://dbOncinha:Expotech2026@cluster0.ydxsizd.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=3000"

try:
    client = MongoClient(MONGO_URL)
    db = client["Oncinha"]
    col = db["ofertas_ia"]
    client.admin.command('ping')
    print("✅ Ounce Stock: Sistema de Ofertas Ativo (Busca por ID)")
except Exception as e:
    print(f"❌ Erro de conexão: {e}")

@app.get("/api/frases/{produto_id}")
async def get_frases(produto_id: int):
    try:
        documento = col.find_one({"id": produto_id})
        if documento and "frases" in documento:
            return {"frases": documento["frases"]}
        return {"frases": ["OFERTA EXCLUSIVA", "APROVEITE AGORA"]}
    except Exception as e:
        return {"frases": ["OUNCE STOCK", "SISTEMA ONLINE"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)