from utils.db import init_pool, execute, query_all
import sys

def update_images():
    try:
        init_pool()
        print("Conectado a la base de datos.")

        # 1. Agregar columna imagen_url si no existe
        try:
            execute("ALTER TABLE recursos ADD COLUMN imagen_url VARCHAR(255) DEFAULT NULL")
            print("Columna 'imagen_url' agregada.")
        except Exception as e:
            if "Duplicate column" in str(e) or "exists" in str(e):
                print("La columna 'imagen_url' ya existe.")
            else:
                print(f"Error al agregar columna: {e}")

        # 2. Mapeo de imágenes
        # Asumimos que las imágenes están en static/img/resources/
        base_path = "/static/img/resources/"
        
        updates = [
            ("%Coworking%", f"{base_path}Coworking_A.jpg"),
            ("%Futbolín%", f"{base_path}Chill_zone_futbolin_A.jpg"),
            ("%Ping Pong%", f"{base_path}Chill_zone_ping_pong.jpg"),
            ("%Billar%", f"{base_path}Chill_zone_billar.jpg"),
            ("%Mesa%", f"{base_path}Coworking_B.jpg"), # Fallback para otras mesas
        ]

        for pattern, image_path in updates:
            sql = "UPDATE recursos SET imagen_url=%s WHERE nombre LIKE %s AND (imagen_url IS NULL OR imagen_url = '')"
            rows = execute(sql, (image_path, pattern))
            print(f"Actualizados {rows} recursos para el patrón '{pattern}' con imagen '{image_path}'")

        print("Actualización de imágenes completada.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    update_images()
