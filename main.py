from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import uvicorn

app = FastAPI()

# Liberação de CORS para o frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração MongoDB 
MONGO_URL = "mongodb+srv://dbOncinha:Expotech2026@cluster0.ydxsizd.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=30000"

try:
    client = MongoClient(MONGO_URL)
    db = client["Oncinha"]
    col = db["ofertas_ia"]
    client.admin.command('ping')
    print("✅ Ounce Stock DB Conectado!")
except Exception as e:
    print(f"❌ Erro no MongoDB: {e}")

@app.get("/api/frases/{produto}")
async def get_frases(produto: str):
    """
    Recebe 'coca', 'guarana' ou 'leite' e busca as frases correspondentes.
    """
    # Mapeia as chaves do frontend para as palavras que estão no seu MongoDB
    mapa_busca = {
        "coca": "Coca-Cola",
        "guarana": "Guaraná",
        "leite": "Leite"
    }
    termo = mapa_busca.get(produto, produto)

    try:
        # Busca no banco usando Regex (ignora se é maiúscula ou minúscula)
        resultado = col.find_one({"produto": {"$regex": termo, "$options": "i"}})
        
        if resultado and "frases" in resultado:
            return {"frases": resultado["frases"]}
        else:
            return {"frases": ["OFERTA ESPECIAL OUNCE STOCK", "CONFIRA!"]}
            
    except Exception as e:
        print(f"Erro na busca: {e}")
        return {"frases": ["SISTEMA DE ESTOQUE", "QUALIDADE GARANTIDA"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)