from notion.client import notion
from database.client import supabase_admin
from notion.schemas import build_notion_properties
from notion.blocks import build_client_second_brain_blocks
from config.settings import settings

def push_to_notion(entity_type: str, entity_id: str, data: dict):
    """
    Sincroniza datos de Supabase a Notion.
    """
    notion_page_id = data.get("notion_page_id") or data.get("notion_block_id")
    props = build_notion_properties(entity_type, data)
    
    # Resolve database ID
    db_map = {
        "client": settings.notion_db_clients,
        "content": settings.notion_db_content,
        "campaign": settings.notion_db_campaigns,
        "decision": settings.notion_db_decisions,
        "metric": settings.notion_db_metrics,
        "asset": settings.notion_db_assets
    }
    database_id = db_map.get(entity_type)
    
    if not database_id:
        print(f"[SYNC] Error: No database mapping for {entity_type}")
        return None

    try:
        if notion_page_id:
            # Update existing
            print(f"[SYNC] Updating Notion page {notion_page_id} for {entity_type} {entity_id}")
            notion.pages.update(page_id=notion_page_id, properties=props)
        else:
            # Create new
            print(f"[SYNC] Creating new Notion page in {database_id} for {entity_type} {entity_id}")
            
            children = []
            if entity_type == "client":
                children = build_client_second_brain_blocks(data)
                
            new_page = notion.pages.create(
                parent={"database_id": database_id},
                properties=props,
                children=children if children else None
            )
            notion_page_id = new_page["id"]
            
            # Update Supabase with Notion ID
            table_map = {
                "client": "clients",
                "content": "content_items"
            }
            table_name = table_map.get(entity_type)
            if table_name:
                col_name = "notion_page_id" if entity_type == "client" else "notion_block_id"
                supabase_admin.table(table_name).update({col_name: notion_page_id}).eq("id", entity_id).execute()
        
        return notion_page_id
    except Exception as e:
        print(f"[SYNC] Error syncing {entity_type} {entity_id}: {str(e)}")
        return None

def get_notion_id(entity_type: str, entity_id: str):
    """
    Fetch Notion ID from Supabase.
    """
    table_map = {
        "client": "clients",
        "content": "content_items"
    }
    table_name = table_map.get(entity_type)
    if not table_name:
        return None
        
    col_name = "notion_page_id" if entity_type == "client" else "notion_block_id"
    res = supabase_admin.table(table_name).select(col_name).eq("id", entity_id).single().execute()
    return res.data.get(col_name) if res.data else None
