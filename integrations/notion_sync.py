import os
import datetime
import sys
from notion_client import Client as NotionClient
from database.client import supabase_admin as supabase
from dotenv import load_dotenv

# Add root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notion.schemas import CLIENT_NOTION_MAP, validate_notion_schema
from config.notifications import notify_error

load_dotenv()

notion = NotionClient(auth=os.getenv("NOTION_TOKEN") or os.getenv("NOTION_API_KEY"))
CLIENTS_DB_ID = os.getenv("NOTION_DB_CLIENTS")
AGENCY_ID = os.getenv("DEFAULT_AGENCY_ID")

def get_rich_text(property_data):
    if not property_data or "rich_text" not in property_data:
        return ""
    return "".join([t["plain_text"] for t in property_data["rich_text"]])

def get_select(property_data):
    if not property_data or "select" not in property_data or not property_data["select"]:
        return None
    return property_data["select"]["name"]

def get_multi_select(property_data):
    if not property_data or "multi_select" not in property_data:
        return []
    return [t["name"] for t in property_data["multi_select"]]

def validate_client_data(data: dict):
    """
    Validates required fields for AI quality.
    """
    required = ["name", "brand_voice", "target_audience", "value_prop", "industry"]
    missing = [field for field in required if not data.get(field) or len(str(data.get(field)).strip()) < 3]
    if missing:
        return False, f"Faltan campos críticos: {', '.join(missing)}"
    return True, None

def update_notion_feedback(page_id: str, status: str, notes: str = ""):
    """
    Writes status and errors back to Notion.
    """
    props = {
        CLIENT_NOTION_MAP["sync_status"]: {"select": {"name": status}},
        CLIENT_NOTION_MAP["system_notes"]: {"rich_text": [{"text": {"content": notes}}]}
    }
    if status == "✅ Sincronizado":
        props[CLIENT_NOTION_MAP["last_sync"]] = {"date": {"start": datetime.datetime.now(datetime.UTC).isoformat()}}
    
    notion.pages.update(page_id=page_id, properties=props)

def sync_notion_to_supabase(notion_page_id: str = None):
    """
    The official 'Judge' sync. Detects pending changes in Notion,
    validates them, and pushes to Supabase.
    """
    print(f"🔍 [JUDGE] Iniciando validación de Notion -> Supabase...")
    
    # 1. Schema Guard
    is_valid, missing = validate_notion_schema(notion, CLIENTS_DB_ID)
    if not is_valid:
        error_msg = f"Esquema de Notion roto. Faltan: {missing}"
        print(f"🚨 {error_msg}")
        notify_error("Schema Guardian", "DATABASE", error_msg)
        return {"error": "schema_broken", "missing": missing}

    try:
        if notion_page_id:
            results = [notion.pages.retrieve(page_id=notion_page_id)]
        else:
            # Query for 'Pendiente' status
            response = notion.databases.query(
                database_id=CLIENTS_DB_ID,
                filter={
                    "property": CLIENT_NOTION_MAP["sync_status"],
                    "select": {"equals": "Pendiente"}
                }
            )
            results = response.get("results", [])
    except Exception as e:
        print(f"❌ Error Notion API: {e}")
        return {"error": str(e)}

    synced = 0
    errors = 0

    for page in results:
        props = page["properties"]
        page_id = page["id"]
        
        # Extract data
        client_data = {
            "name": get_rich_text(props.get(CLIENT_NOTION_MAP["name"])) if "title" in props.get(CLIENT_NOTION_MAP["name"], {}) else get_rich_text(props.get(CLIENT_NOTION_MAP["name"])), # title vs rich_text
            "industry": get_select(props.get(CLIENT_NOTION_MAP["industry"])),
            "brand_voice": get_rich_text(props.get(CLIENT_NOTION_MAP["brand_voice"])),
            "target_audience": get_rich_text(props.get(CLIENT_NOTION_MAP["target_audience"])),
            "value_prop": get_rich_text(props.get(CLIENT_NOTION_MAP["value_prop"])),
            "competition": get_rich_text(props.get(CLIENT_NOTION_MAP["competition"])),
            "strategy": get_rich_text(props.get(CLIENT_NOTION_MAP["strategy"])),
            "dos": get_multi_select(props.get(CLIENT_NOTION_MAP["dos"])),
            "donts": get_multi_select(props.get(CLIENT_NOTION_MAP["donts"])),
            "brand_colors": get_multi_select(props.get(CLIENT_NOTION_MAP["brand_colors"])),
            "fonts": get_multi_select(props.get(CLIENT_NOTION_MAP["fonts"])),
            "briefing_url": props.get(CLIENT_NOTION_MAP["briefing_url"], {}).get("url"),
            "brand_manual_url": props.get(CLIENT_NOTION_MAP["brand_manual_url"], {}).get("url"),
            "notion_page_id": page_id,
            "status": "active"
        }
        
        # Correcting 'name' extraction for Title properties
        if props[CLIENT_NOTION_MAP["name"]]["type"] == "title":
            client_data["name"] = "".join([t["plain_text"] for t in props[CLIENT_NOTION_MAP["name"]]["title"]])

        # 2. Validation
        is_valid, err_msg = validate_client_data(client_data)
        if not is_valid:
            update_notion_feedback(page_id, "❌ Error", err_msg)
            errors += 1
            continue

        # 3. Sync to Supabase
        try:
            client_data["slug"] = client_data["name"].lower().replace(" ", "-")
            client_data["agency_id"] = AGENCY_ID
            
            res = supabase.table("clients").upsert(client_data, on_conflict="notion_page_id").execute()
            supabase_id = res.data[0]["id"]
            
            # 4. Success Feedback
            update_notion_feedback(page_id, "✅ Sincronizado", "Contexto IA actualizado correctamente.")
            # Update Supabase ID in Notion if missing
            notion.pages.update(page_id=page_id, properties={
                CLIENT_NOTION_MAP["supabase_id"]: {"rich_text": [{"text": {"content": supabase_id}}]}
            })
            synced += 1
        except Exception as e:
            update_notion_feedback(page_id, "❌ Error", f"DB Error: {str(e)}")
            errors += 1

    return {"synced": synced, "errors": errors}

if __name__ == "__main__":
    sync_notion_to_supabase()
