import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID")
DB_CLIENTS_ID = os.getenv("NOTION_DB_CLIENTS")

def main():
    # 1. Actualizar base de Clientes con las columnas de las imágenes
    print("Actualizando base de Clientes con columnas de tracking...")
    new_props = {
        "EQUIPO": {"select": {"options": [
            {"name": "Shantu & Danna", "color": "purple"},
            {"name": "Valen & Cami I", "color": "orange"},
            {"name": "Caro", "color": "blue"}
        ]}},
        "DISEÑADO FEED HASTA": {"date": {}},
        "PROGRAMADO HASTA": {"date": {}},
        "HISTORIAS HASTA": {"date": {}},
        "DISEÑADORA": {"select": {"options": [
            {"name": "DANNA", "color": "purple"},
            {"name": "SHANTU", "color": "blue"},
            {"name": "VALEN", "color": "orange"},
            {"name": "CAMI", "color": "green"}
        ]}},
        "COMMUNITY": {"select": {"options": [
            {"name": "SHANTU", "color": "blue"},
            {"name": "DANNA", "color": "purple"},
            {"name": "VALEN", "color": "orange"},
            {"name": "CAMI", "color": "green"}
        ]}},
        "META ADS": {"select": {"options": [
            {"name": "SI", "color": "green"},
            {"name": "NO", "color": "red"}
        ]}},
        "MAILING": {"select": {"options": [
            {"name": "SI", "color": "green"},
            {"name": "NO", "color": "red"}
        ]}}
    }
    notion.databases.update(database_id=DB_CLIENTS_ID, properties=new_props)

    # 2. Crear la jerarquía de páginas en el Sidebar
    print("Creando jerarquía de Equipos en el Sidebar...")
    
    # Crear página "Equipos"
    equipos_page = notion.pages.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        properties={
            "title": {"title": [{"text": {"content": "👥 Equipos"}}]}
        },
        icon={"type": "emoji", "emoji": "👥"}
    )
    equipos_id = equipos_page["id"]

    # Crear página de equipo "Shantu & Danna"
    # Nota: No podemos crear vistas vinculadas complejas por API fácilmente, 
    # pero podemos dejar la página lista con un encabezado.
    team_page = notion.pages.create(
        parent={"type": "page_id", "page_id": equipos_id},
        properties={
            "title": {"title": [{"text": {"content": "👭 Shantu & Danna"}}]}
        },
        icon={"type": "emoji", "emoji": "👭"}
    )

    print("\n✅ Estructura refinada con éxito.")
    print("Columnas de tracking añadidas a Clientes.")
    print(f"Página Equipos creada: {equipos_id}")

if __name__ == "__main__":
    main()
