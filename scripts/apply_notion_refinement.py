import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID")
DB_CLIENTS_ID = os.getenv("NOTION_DB_CLIENTS")
DB_CONTENT_ID = os.getenv("NOTION_DB_CONTENT")

def update_databases():
    print("Updating Clientes database properties...")
    clients_props = {
        "EQUIPO": {"select": {"options": [
            {"name": "Team Sofi & Ori", "color": "purple"},
            {"name": "Team Flor & Angie", "color": "orange"},
            {"name": "Team Caro", "color": "blue"}
        ]}},
        "HISTORIAS": {"select": {"options": [
            {"name": "TODOS LOS DIAS", "color": "green"},
            {"name": "DIA POR MEDIO", "color": "yellow"},
            {"name": "NO", "color": "red"}
        ]}},
        "POSTEOS / SEMANA": {"number": {"format": "number"}},
        "UBICACIÓN / WHATSAPP": {"url": {}},
        "WEB": {"url": {}},
        "DISEÑADORA": {"select": {"options": [
            {"name": "SOFI", "color": "purple"},
            {"name": "ORI", "color": "blue"},
            {"name": "FLOR", "color": "orange"},
            {"name": "ANGIE", "color": "green"}
        ]}},
        "COMMUNITY": {"select": {"options": [
            {"name": "SOFI", "color": "purple"},
            {"name": "ORI", "color": "blue"},
            {"name": "FLOR", "color": "orange"},
            {"name": "ANGIE", "color": "green"}
        ]}}
    }
    notion.databases.update(database_id=DB_CLIENTS_ID, properties=clients_props)

    print("Updating Content database properties...")
    content_props = {
        "Status": {"select": {"options": [
            {"name": "Planning", "color": "gray"},
            {"name": "In Progress", "color": "blue"},
            {"name": "Review", "color": "yellow"},
            {"name": "Completed", "color": "green"}
        ]}},
        "assigned_cm": {"select": {"options": [
            {"name": "SOFI", "color": "purple"},
            {"name": "ORI", "color": "blue"},
            {"name": "FLOR", "color": "orange"},
            {"name": "ANGIE", "color": "green"}
        ]}},
        "assigned_designer": {"select": {"options": [
            {"name": "SOFI", "color": "purple"},
            {"name": "ORI", "color": "blue"},
            {"name": "FLOR", "color": "orange"},
            {"name": "ANGIE", "color": "green"}
        ]}},
        "designed_until": {"date": {}},
        "programmed_until": {"date": {}}
    }
    notion.databases.update(database_id=DB_CONTENT_ID, properties=content_props)

def create_hierarchy():
    print("Creating sidebar hierarchy...")
    
    # Check if Equipos already exists to avoid duplicates
    # For simplicity in this script, we'll just create it. 
    # In a real scenario, we'd search first.
    
    equipos_page = notion.pages.create(
        parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
        properties={"title": {"title": [{"text": {"content": "👥 Equipos"}}]}},
        icon={"type": "emoji", "emoji": "👥"}
    )
    equipos_id = equipos_page["id"]

    teams = [
        {"name": "Team Sofi & Ori", "emoji": "👭"},
        {"name": "Team Flor & Angie", "emoji": "👭"},
        {"name": "Team Caro", "emoji": "👩"}
    ]

    for team in teams:
        notion.pages.create(
            parent={"type": "page_id", "page_id": equipos_id},
            properties={"title": {"title": [{"text": {"content": team["name"]}}]}},
            icon={"type": "emoji", "emoji": team["emoji"]}
        )

    # Create other support pages
    support_pages = [
        {"name": "Acceso", "emoji": "🔐"},
        {"name": "Edición", "emoji": "🎨"},
        {"name": "Influencers", "emoji": "📢"},
        {"name": "HOT SALE", "emoji": "🔥"},
        {"name": "Creación de Contenido", "emoji": "✍️"}
    ]

    for p in support_pages:
        notion.pages.create(
            parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
            properties={"title": {"title": [{"text": {"content": p["name"]}}]}},
            icon={"type": "emoji", "emoji": p["emoji"]}
        )

def main():
    try:
        update_databases()
        create_hierarchy()
        print("\n✅ Notion refinement applied successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
