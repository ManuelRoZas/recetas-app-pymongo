from bson.objectid import ObjectId
from datetime import datetime

def mostrar_comentarios(db):
    print("\n--- COMENTARIOS ---")
    for c in db.comentarios.find():
        autor = db.usuarios.find_one({"_id": c["autorId"]})
        receta = db.recetas.find_one({"_id": c["recetaId"]})
        nombre_autor = autor["nombre"] if autor else "Autor desconocido"
        titulo_receta = receta["titulo"] if receta else "Receta desconocida"
        calificacion = c.get("calificacion", "Sin calificación")
        print(f"{nombre_autor} comentó en '{titulo_receta}': {c['texto']} ({calificacion}/5)")

def comentar_receta(db, usuario):
    titulo = input("Título de la receta a comentar: ").strip()
    receta = db.recetas.find_one({"titulo": titulo})

    if receta:
        texto = input("Comentario: ").strip()
        try:
            calificacion = int(input("Calificación (1 a 5, opcional - enter para omitir): ").strip())
        except ValueError:
            calificacion = None

        comentario = {
            "recetaId": receta["_id"],
            "autorId": usuario["_id"],
            "texto": texto,
            "calificacion": calificacion,
            "fecha": datetime.now()
        }
        resultado = db.comentarios.insert_one(comentario)
        print(f"Comentario publicado con ID: {resultado.inserted_id}")
        return resultado.inserted_id
    else:
        print("No se encontró receta con ese título.")
        return None

