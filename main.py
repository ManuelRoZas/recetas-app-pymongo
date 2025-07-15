from bson.objectid import ObjectId
from controllers import usuarios_controller, recetas_controller, comentarios_controller
from pymongo import MongoClient

def menu_inicio(db):
    while True:
        print("\n--- BIENVENIDO ---")
        print("1. Ingresar usuario")
        print("2. Crear usuario")
        print("0. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            usuario = usuarios_controller.ingresar_usuario(db)
            if usuario:
                return usuario

        elif opcion == "2":
            usuarios_controller.crear_usuario_interactivo(db)
        elif opcion == "0":
            print("¡Hasta luego!")
            return None
        else:
            print("Opción inválida, intentá de nuevo.")

def menu_principal(db, usuario):
    while True:
        print(f"\n--- MENÚ RECETAS (Usuario: {usuario['nombre']}) ---")
        print("1. Ver usuarios")
        print("2. Ver recetas")
        print("3. Ver comentarios")
        print("4. Publicar receta")
        print("5. Buscar receta por ingrediente")
        print("6. Dar/Quitar like a receta")
        print("7. Comentar receta")
        print("8. Ver top recetas")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            usuarios_controller.mostrar_usuarios(db)

        elif opcion == "2":
            recetas_controller.mostrar_recetas(db)

        elif opcion == "3":
            comentarios_controller.mostrar_comentarios(db)

        elif opcion == "4":
            recetas_controller.publicar_receta(db, usuario['_id'])

        elif opcion == "5":
            recetas_controller.buscar_por_ingrediente(db)

        elif opcion == "6":
            recetas_controller.dar_like(db)

        elif opcion == "7":
            comentarios_controller.comentar_receta(db, usuario)

        elif opcion == "8":
            recetas_controller.top_recetas(db)
        elif opcion == "0":
            print("¡Chau!")
            break

        else:
            print("Opción inválida, intentá de nuevo.")

def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.recetasdb

    usuario = menu_inicio(db)
    if usuario:
        menu_principal(db, usuario)

    client.close()

if __name__ == "__main__":
    main()
