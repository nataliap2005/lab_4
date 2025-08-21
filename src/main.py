from create_db import run as create_schema
from load_db import load_all

def main():
    print("🚀 Creando base y tablas...")
    create_schema()
    print("✔ Esquema creado.")

    print("📥 Cargando datos desde CSV...")
    load_all()
    print("✔ Datos cargados.")

if __name__ == "__main__":
    main()
