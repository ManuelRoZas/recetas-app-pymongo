from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def seed_data():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(MONGO_URI)
    db = client.recetasdb
    print("Bases de datos en servidor:", client.list_database_names())
    print("Usando base:", db.name)

    db.usuarios.delete_many({})
    db.recetas.delete_many({})
    db.comentarios.delete_many({})
    
    
    usuario = {
        "nombre": "Chef Ana",
        "email": "ana@chef.com",
        "nivel": "Intermedio",
        "recetasPublicadas": 15,
        "seguidores": 234
    }
    usuario_resultado = db.usuarios.insert_one(usuario)
    usuario_id = usuario_resultado.inserted_id
    print("Insertado usuario con ID:", usuario_resultado.inserted_id)

    # Insertar receta
    receta = {
        "titulo": "Paella Valenciana",
        "descripcion": "Receta tradicional española",
        "autorId": usuario_id,
        "ingredientes": [
            {"nombre": "arroz", "cantidad": "400g"},
            {"nombre": "pollo", "cantidad": "1 kg"}
        ],
        "instrucciones": ["Paso 1...", "Paso 2..."],
        "tiempoCoccion": 45,
        "dificultad": "Media",
        "tipoCocina": "Española",
        "likes": 127,
        "fechaPublicacion": datetime.now()
    }
    receta_resultado = db.recetas.insert_one(receta)
    receta_id = receta_resultado.inserted_id
    print("Insertado receta con ID:", receta_resultado.inserted_id)

    # Insertar comentario
    comentario = {
        "recetaId": receta_id,
        "autorId": usuario_id,
        "texto": "¡Deliciosa receta!",
        "calificacion": 5,
        "fecha": datetime.now()
    }
    comentario_resultado = db.comentarios.insert_one(comentario)
    print("Insertado comentario con ID:", comentario_resultado.inserted_id)

    print("Seed completado con éxito.")

    client.close()

if __name__ == "__main__":
    seed_data()