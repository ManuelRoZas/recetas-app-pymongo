from bson.objectid import ObjectId

def mostrar_usuarios(db):
    print("\n--- USUARIOS ---")
    for u in db.usuarios.find():
        print(f"{u['_id']} - {u['nombre']} ({u['nivel']}) - {u['email']}")


def obtener_por_email(db, email):
    usuario = db.usuarios.find_one({"email": email})
    return usuario

def ingresar_usuario(db):
    email = input("Email: ").strip()
    usuario = db.usuarios.find_one({"email": email})
    if usuario:
        print(f"Bienvenido, {usuario['nombre']}!")
        return usuario
    else:
        print("Usuario no encontrado.")
        return None

def crear_usuario_interactivo(db):
    nombre = input("Nombre: ").strip()
    email = input("Email: ").strip()
    nivel = input("Nivel (Principiante, Intermedio, Avanzado): ").strip()
    usuario_nuevo = {
        "nombre": nombre,
        "email": email,
        "nivel": nivel,
        "recetasPublicadas": 0,
        "seguidores": 0
    }
    resultado = db.usuarios.insert_one(usuario_nuevo)
    print(f"Usuario creado con ID: {resultado.inserted_id}")
    return resultado.inserted_id