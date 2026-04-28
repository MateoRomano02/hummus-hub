import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID")

def create_database(parent_id, title, properties, icon="🏢"):
    print(f"Creando base de datos: {title}...")
    return notion.databases.create(
        parent={"type": "page_id", "page_id": parent_id},
        title=[{"type": "text", "text": {"content": title}}],
        icon={"type": "emoji", "emoji": icon},
        properties=properties
    )

def main():
    # 1. Base de datos: Clientes
    clientes_props = {
        "Nombre": {"title": {}},
        "Slug": {"rich_text": {}},
        "Status": {"select": {"options": [
            {"name": "Active", "color": "green"},
            {"name": "Onboarding", "color": "blue"},
            {"name": "Inactive", "color": "red"}
        ]}},
        "Email": {"email": {}},
        "WhatsApp": {"phone_number": {}},
        "Website": {"url": {}},
        "Instagram": {"url": {}},
        "Industria": {"rich_text": {}},
        "Voz de Marca": {"rich_text": {}},
        "Propuesta de Valor": {"rich_text": {}},
        "Drive Folder": {"url": {}},
        "ID Supabase": {"rich_text": {}}
    }
    clientes_db = create_database(PARENT_PAGE_ID, "🏢 Clientes", clientes_props, "🏢")
    clientes_id = clientes_db["id"]

    # 2. Base de datos: Campañas
    campanas_props = {
        "Nombre": {"title": {}},
        "Cliente": {"relation": {"database_id": clientes_id, "single_property": {}}},
        "Status": {"select": {"options": [
            {"name": "Planning", "color": "gray"},
            {"name": "Active", "color": "green"},
            {"name": "Completed", "color": "blue"},
            {"name": "Paused", "color": "yellow"}
        ]}},
        "Inicio": {"date": {}},
        "Fin": {"date": {}},
        "Objetivo": {"rich_text": {}},
        "Drive URL": {"url": {}},
        "ID Supabase": {"rich_text": {}}
    }
    campanas_db = create_database(PARENT_PAGE_ID, "📅 Campañas", campanas_props, "📅")
    campanas_id = campanas_db["id"]

    # 3. Base de datos: Contenido
    contenido_props = {
        "Nombre": {"title": {}},
        "Cliente": {"relation": {"database_id": clientes_id, "single_property": {}}},
        "Campaña": {"relation": {"database_id": campanas_id, "single_property": {}}},
        "Plataforma": {"select": {"options": [
            {"name": "Instagram", "color": "pink"},
            {"name": "Meta Ads", "color": "blue"},
            {"name": "Google Ads", "color": "yellow"},
            {"name": "TikTok", "color": "black"},
            {"name": "LinkedIn", "color": "blue"}
        ]}},
        "Tipo": {"select": {"options": [
            {"name": "Post", "color": "gray"},
            {"name": "Story", "color": "orange"},
            {"name": "Reel", "color": "purple"},
            {"name": "Ad", "color": "red"},
            {"name": "Carousel", "color": "green"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "Planning", "color": "gray"},
            {"name": "Copywriting", "color": "blue"},
            {"name": "Design", "color": "purple"},
            {"name": "Audit", "color": "yellow"},
            {"name": "Programmed", "color": "green"},
            {"name": "Published", "color": "green"}
        ]}},
        "Copy": {"rich_text": {}},
        "Programado para": {"date": {}},
        "Publicado el": {"date": {}},
        "ID Supabase": {"rich_text": {}}
    }
    contenido_db = create_database(PARENT_PAGE_ID, "✍️ Contenido", contenido_props, "✍️")

    # 4. Base de datos: Decisiones
    decisiones_props = {
        "Contenido": {"title": {}},
        "Cliente": {"relation": {"database_id": clientes_id, "single_property": {}}},
        "Campaña": {"relation": {"database_id": campanas_id, "single_property": {}}},
        "Fuente": {"select": {"options": [
            {"name": "Meeting", "color": "blue"},
            {"name": "WhatsApp", "color": "green"},
            {"name": "Email", "color": "gray"},
            {"name": "Notion", "color": "black"}
        ]}},
        "Fecha": {"date": {}},
        "Decidido por": {"rich_text": {}},
        "Contexto": {"rich_text": {}},
        "ID Supabase": {"rich_text": {}}
    }
    decisiones_db = create_database(PARENT_PAGE_ID, "⚖️ Decisiones", decisiones_props, "⚖️")

    # 5. Base de datos: Métricas
    metricas_props = {
        "Periodo": {"title": {}},
        "Cliente": {"relation": {"database_id": clientes_id, "single_property": {}}},
        "Plataforma": {"select": {"options": [
            {"name": "Instagram", "color": "pink"},
            {"name": "Meta Ads", "color": "blue"},
            {"name": "Google Ads", "color": "yellow"}
        ]}},
        "Reach": {"number": {"format": "number"}},
        "Interactions": {"number": {"format": "number"}},
        "Impressions": {"number": {"format": "number"}},
        "Spend": {"number": {"format": "dollar"}},
        "ROAS": {"number": {"format": "number"}},
        "Followers End": {"number": {"format": "number"}},
        "ID Supabase": {"rich_text": {}}
    }
    metricas_db = create_database(PARENT_PAGE_ID, "📊 Métricas", metricas_props, "📊")

    # 6. Base de datos: Assets
    assets_props = {
        "Asset": {"title": {}},
        "Cliente": {"relation": {"database_id": clientes_id, "single_property": {}}},
        "Tipo": {"select": {"options": [
            {"name": "Logo", "color": "gray"},
            {"name": "Photo", "color": "blue"},
            {"name": "Video", "color": "purple"},
            {"name": "PDF Manual", "color": "red"},
            {"name": "Font", "color": "yellow"}
        ]}},
        "Drive URL": {"url": {}},
        "Label": {"rich_text": {}},
        "ID Supabase": {"rich_text": {}}
    }
    assets_db = create_database(PARENT_PAGE_ID, "🖼 Assets", assets_props, "🖼")

    # 7. Base de datos: Calendario
    calendario_props = {
        "Evento": {"title": {}},
        "Fecha": {"date": {}},
        "Recurrente": {"checkbox": {}},
        "Tipo": {"select": {"options": [
            {"name": "Holiday", "color": "green"},
            {"name": "Launch", "color": "red"},
            {"name": "Event", "color": "blue"}
        ]}},
        "ID Supabase": {"rich_text": {}}
    }
    calendario_db = create_database(PARENT_PAGE_ID, "🎊 Calendario", calendario_props, "🎊")

    print("\n✅ Estructura de Notion creada con éxito.")
    print(f"Database Clientes ID: {clientes_id}")
    print(f"Database Campañas ID: {campanas_id}")

if __name__ == "__main__":
    main()
