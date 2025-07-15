from bson.objectid import ObjectId
from datetime import datetime

def mostrar_recetas(db):
    recetas = db.recetas.find()
    for r in recetas:
        autor = db.usuarios.find_one({"_id": r["autorId"]})
        nombre_autor = autor["nombre"] if autor else "Desconocido"
        print(f"{r['_id']} - {r['titulo']} (por {nombre_autor}) - {r['likes']} likes")

def publicar_receta(db, autor_id):
    titulo = input("Título: ").strip()
    descripcion = input("Descripción: ").strip()
    
    ingredientes_input = input("Ingredientes (nombre:cantidad separados por coma): ")
    ingredientes = []
    for item in ingredientes_input.split(","):
        try:
            nombre, cantidad = item.split(":")
            ingredientes.append({"nombre": nombre.strip(), "cantidad": cantidad.strip()})
        except ValueError:
            print(f"Ingrediente mal formateado: {item}")

    instrucciones = input("Instrucciones (separadas por punto y coma): ").split(";")
    instrucciones = [i.strip() for i in instrucciones if i.strip()]

    try:
        tiempo_coccion = int(input("Tiempo de cocción (minutos): "))
    except ValueError:
        print("Tiempo inválido. Usando 0.")
        tiempo_coccion = 0

    dificultad = input("Dificultad (Fácil, Media, Difícil): ").strip()
    tipo_cocina = input("Tipo de cocina: ").strip()

    receta = {
        "titulo": titulo,
        "descripcion": descripcion,
        "autorId": ObjectId(autor_id),
        "ingredientes": ingredientes,
        "instrucciones": instrucciones,
        "tiempoCoccion": tiempo_coccion,
        "dificultad": dificultad,
        "tipoCocina": tipo_cocina,
        "likes": 0,
        "fechaPublicacion": datetime.now()
    }

    resultado = db.recetas.insert_one(receta)
    print(f"Receta publicada con ID: {resultado.inserted_id}")
    return resultado.inserted_id

def buscar_por_ingrediente(db):
    ingrediente = input("Ingrese el nombre del ingrediente: ").strip()
    recetas = list(db.recetas.find({"ingredientes.nombre": ingrediente}))

    if len(recetas) == 0:
        print(f"No se encontraron recetas con el ingrediente '{ingrediente}'.")
    else:
        print(f"Recetas que contienen '{ingrediente}':")
        for r in recetas:
            autor = db.usuarios.find_one({"_id": r["autorId"]})
            nombre_autor = autor["nombre"] if autor else "Desconocido"
            print(f"{r['_id']} - {r['titulo']} (por {nombre_autor}) - {r['likes']} likes")

    return recetas

from bson.objectid import ObjectId

def dar_like(db):
    titulo = input("Título de la receta para dar/quitar like: ").strip()
    receta = db.recetas.find_one({"titulo": titulo})

    if receta:
        accion = input("Dar like? (s/n): ").lower()
        dar_like = accion == "s"
        incremento = 1 if dar_like else -1

        resultado = db.recetas.update_one(
            {"_id": receta["_id"]},
            {"$inc": {"likes": incremento}}
        )

        if resultado.modified_count > 0:
            print("Like actualizado correctamente.")
        else:
            print("No se pudo actualizar el like.")
    else:
        print("No se encontró receta con ese título.")


def comentar_receta(db, receta_id, autor_id, texto_comentario, calificacion=None):
    comentario = {
        "recetaId": ObjectId(receta_id),
        "autorId": ObjectId(autor_id),
        "texto": texto_comentario,
        "calificacion": calificacion,
        "fecha": datetime.now()
    }
    resultado = db.comentarios.insert_one(comentario)
    print(f"Comentario publicado con ID: {resultado.inserted_id}")
    return resultado.inserted_id

def top_recetas(db, top_n=5):
    recetas = db.recetas.find().sort("likes", -1).limit(top_n)
    return list(recetas)
