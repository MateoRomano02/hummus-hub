import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HUB_PAGE_ID = "350aa2e860408058891fea1f3a4a72de"
CLIENTS_DB_ID = "6273c3db-e547-4b4d-beef-af0e14b1fb3d"
CONTENT_DB_ID = "60f2a9a3-3518-4135-9b60-ba5b229814fd"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def update_db(db_id, properties):
    url = f"https://api.notion.com/v1/databases/{db_id}"
    data = {"properties": properties}
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

def create_db(parent_id, title, properties, icon_emoji):
    url = "https://api.notion.com/v1/databases"
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [{"type": "text", "text": {"content": title}}],
        "icon": {"type": "emoji", "emoji": icon_emoji},
        "properties": properties
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def run():
    print("Updating Clientes database with strategy and sync fields...")
    clients_props = {
        "📅 Comienzo": {"date": {}},
        "📋 Rubro": {"select": {"options": [
            {"name": "Moda", "color": "pink"},
            {"name": "Gastronomía", "color": "orange"},
            {"name": "Tecnología", "color": "blue"},
            {"name": "Servicios", "color": "gray"},
            {"name": "E-commerce", "color": "green"}
        ]}},
        "📈 Plan": {"multi_select": {"options": [
            {"name": "Redes Sociales", "color": "purple"},
            {"name": "Email Marketing", "color": "yellow"},
            {"name": "Paid Media (Ads)", "color": "red"},
            {"name": "Branding & Diseño", "color": "blue"},
            {"name": "Estrategia IA", "color": "green"}
        ]}},
        "🎯 Público Objetivo": {"rich_text": {}},
        "📝 Descripción": {"rich_text": {}},
        "🔗 Manual de Marca": {"url": {}},
        "📂 Briefing": {"url": {}},
        "🔄 Sync Trigger": {"checkbox": {}},
        "⌛ Last Sync": {"date": {}},
        "🆔 Supabase ID": {"rich_text": {}}
    }
    update_db(CLIENTS_DB_ID, clients_props)

    print("Creating Agent Logs database...")
    logs_props = {
        "Log Name": {"title": {}},
        "🤖 Agente": {"select": {"options": [
            {"name": "Account Manager", "color": "blue"},
            {"name": "Creative Agent", "color": "purple"},
            {"name": "Strategy Agent", "color": "green"},
            {"name": "Auditor Agent", "color": "red"}
        ]}},
        "Status": {"select": {"options": [
            {"name": "Running", "color": "yellow"},
            {"name": "Success", "color": "green"},
            {"name": "Error", "color": "red"}
        ]}},
        "Cliente": {"relation": {"database_id": CLIENTS_DB_ID}},
        "Timestamp": {"date": {}},
        "Log Detail": {"rich_text": {}},
        "Prompt Hash": {"rich_text": {}}
    }
    logs_db = create_db(HUB_PAGE_ID, "🤖 Bitácora de Agentes", logs_props, "🤖")
    
    print("Creating Knowledge Base (Second Brain) database...")
    kb_props = {
        "Knowledge Item": {"title": {}},
        "Tipo": {"select": {"options": [
            {"name": "Briefing", "color": "blue"},
            {"name": "Tono de Voz", "color": "purple"},
            {"name": "Audiencia", "color": "green"},
            {"name": "Competencia", "color": "red"},
            {"name": "Insight", "color": "yellow"}
        ]}},
        "Cliente": {"relation": {"database_id": CLIENTS_DB_ID}},
        "Contenido": {"rich_text": {}},
        "Tags": {"multi_select": {}}
    }
    kb_db = create_db(HUB_PAGE_ID, "🧠 Second Brain (Knowledge)", kb_props, "🧠")

    print("Updating Content database with agentic fields...")
    content_props = {
        "Status": {"select": {"options": [
            {"name": "Ideas", "color": "gray"},
            {"name": "Draft (AI)", "color": "orange"},
            {"name": "Review", "color": "yellow"},
            {"name": "Design", "color": "purple"},
            {"name": "Approved", "color": "green"},
            {"name": "Programmed", "color": "blue"}
        ]}},
        "Cliente": {"relation": {"database_id": CLIENTS_DB_ID}},
        "AI Output": {"rich_text": {}},
        "Designed Until": {"date": {}},
        "Programmed Until": {"date": {}}
    }
    update_db(CONTENT_DB_ID, content_props)

    print("Infrastructure update complete.")

if __name__ == "__main__":
    run()
