import os
import datetime
from notion_client import Client as NotionClient
from config.supabase_client import supabase
from dotenv import load_dotenv

load_dotenv()

notion = NotionClient(auth=os.getenv("NOTION_TOKEN"), notion_version="2022-06-28")
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

def sync_notion_to_supabase():
    """
    Finds clients in Notion with 'Sync Trigger' enabled and updates Supabase.
    """
    print("Starting Notion -> Supabase sync...")
    
    # 1. Query Notion for pages with Sync Trigger = True
    try:
        response = notion.request(
            path=f"databases/{CLIENTS_DB_ID}/query",
            method="POST",
            body={
                "filter": {
                    "property": "🔄 Sync Trigger",
                    "checkbox": {
                        "equals": True
                    }
                }
            }
        )
    except Exception as e:
        print(f"Error querying Notion: {e}")
        return {"error": str(e)}

    results = response.get("results", [])
    print(f"Found {len(results)} clients to sync.")

    synced_count = 0
    for page in results:
        props = page["properties"]
        page_id = page["id"]
        
        # Extract name (Title)
        name = ""
        if "Name" in props and props["Name"]["title"]:
            name = props["Name"]["title"][0]["plain_text"]
        
        if not name:
            continue

        # Map properties
        client_data = {
            "agency_id": AGENCY_ID,
            "name": name,
            "slug": name.lower().replace(" ", "-"),  # Simple slug generation
            "industry": get_select(props.get("📋 Rubro")),
            "target_audience": get_rich_text(props.get("🎯 Público Objetivo")),
            "brand_identity": props.get("🔗 Manual de Marca", {}).get("url"),
            "briefing_url": props.get("📂 Briefing", {}).get("url"),
            "start_date": props.get("📅 Comienzo", {}).get("date", {}).get("start") if props.get("📅 Comienzo", {}).get("date") else None,
            "notion_page_id": page_id,
            "extra": {
                "plan": get_multi_select(props.get("📈 Plan")),
                "description": get_rich_text(props.get("📝 Descripción")),
            },
            "updated_at": datetime.datetime.now(datetime.UTC).isoformat()
        }

        # 2. Upsert to Supabase
        try:
            # Use notion_page_id as unique constraint
            res = supabase.table("clients").upsert(client_data, on_conflict="notion_page_id").execute()
            supabase_id = res.data[0]["id"]
            print(f"Synced {name} to Supabase with ID: {supabase_id}")
            
            # 3. Update Notion (Uncheck Trigger, set Last Sync, set Supabase ID)
            notion.pages.update(
                page_id=page_id,
                properties={
                    "🔄 Sync Trigger": {"checkbox": False},
                    "⌛ Last Sync": {"date": {"start": datetime.datetime.now(datetime.UTC).isoformat()}},
                    "🆔 Supabase ID": {"rich_text": [{"text": {"content": supabase_id}}]}
                }
            )
            synced_count += 1
        except Exception as e:
            print(f"Error syncing client {name}: {e}")

    return {"status": "ok", "synced": synced_count}

if __name__ == "__main__":
    sync_notion_to_supabase()
