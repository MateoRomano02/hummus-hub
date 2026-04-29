from datetime import datetime

# Centralized mapping for Notion <-> Supabase
# This is the "Source of Truth" for property names in Notion.
# If a property is renamed in Notion, it MUST be updated here.
CLIENT_NOTION_MAP = {
    "name": "Name",
    "description": "📝 Descripción",
    "industry": "📋 Rubro",
    "team": "👥 Equipo",
    "supabase_id": "🆔 Supabase ID",
    "brand_voice": "🗣️ Tono de Voz",
    "target_audience": "🎯 Público Objetivo",
    "value_prop": "✨ Propuesta de Valor",
    "competition": "🥊 Competencia",
    "strategy": "💡 Estrategia",
    "dos": "✅ Dos",
    "donts": "❌ Donts",
    "brand_colors": "🎨 Colores",
    "fonts": "🔤 Tipografías",
    "stories_freq": "📱 Frecuencia Stories",
    "posts_per_week": "📅 Posts x Semana",
    "briefing_url": "📂 Briefing",
    "brand_manual_url": "🔗 Manual de Marca",
    "plan": "📈 Plan",
    "start_date": "📅 Comienzo",
    "sync_status": "🔄 Estado de Sync",
    "system_notes": "📝 Notas del Sistema",
    "last_sync": "⌛ Last Sync"
}

def validate_notion_schema(notion_client, database_id: str):
    """
    Checks if the Notion database has all the required properties from CLIENT_NOTION_MAP.
    Returns (is_valid, missing_properties)
    """
    try:
        db = notion_client.databases.retrieve(database_id=database_id)
        existing_props = db.get("properties", {}).keys()
        required_props = set(CLIENT_NOTION_MAP.values())
        
        missing = required_props - set(existing_props)
        return len(missing) == 0, list(missing)
    except Exception as e:
        print(f"Error validating Notion schema: {e}")
        return False, [str(e)]

# Notion property mapping schemas
def build_notion_properties(entity_type: str, data: dict):
    """
    Builds the property object for the Notion API based on entity type and raw data.
    """
    if entity_type == "client":
        # Extract fields from 'extra' or direct
        extra = data.get("extra", {})
        plan = extra.get("plan", [])
        
        props = {
            CLIENT_NOTION_MAP["name"]: {"title": [{"text": {"content": data.get("name", "Unknown")}}]},
            CLIENT_NOTION_MAP["description"]: {"rich_text": [{"text": {"content": data.get("description", "") or ""}}]},
            CLIENT_NOTION_MAP["industry"]: {"select": {"name": data.get("industry", "Servicios") or "Servicios"}},
            CLIENT_NOTION_MAP["team"]: {"select": {"name": data.get("team", "Team Sofi & Ori") or "Team Sofi & Ori"}},
            CLIENT_NOTION_MAP["supabase_id"]: {"rich_text": [{"text": {"content": str(data.get("id", ""))}}]},
            CLIENT_NOTION_MAP["brand_voice"]: {"rich_text": [{"text": {"content": data.get("brand_voice", "") or ""}}]},
            CLIENT_NOTION_MAP["target_audience"]: {"rich_text": [{"text": {"content": data.get("target_audience", "") or ""}}]},
            CLIENT_NOTION_MAP["value_prop"]: {"rich_text": [{"text": {"content": data.get("value_prop", "") or ""}}]},
            CLIENT_NOTION_MAP["competition"]: {"rich_text": [{"text": {"content": data.get("competition", "") or ""}}]},
            CLIENT_NOTION_MAP["strategy"]: {"rich_text": [{"text": {"content": data.get("strategy", "") or ""}}]},
            CLIENT_NOTION_MAP["dos"]: {"multi_select": [{"name": d} for d in data.get("dos", [])]},
            CLIENT_NOTION_MAP["donts"]: {"multi_select": [{"name": d} for d in data.get("donts", [])]},
            CLIENT_NOTION_MAP["brand_colors"]: {"multi_select": [{"name": c} for c in data.get("brand_colors", [])]},
            CLIENT_NOTION_MAP["fonts"]: {"multi_select": [{"name": f} for f in data.get("fonts", [])]},
            CLIENT_NOTION_MAP["stories_freq"]: {"select": {"name": data.get("stories_freq")}} if data.get("stories_freq") else None,
            CLIENT_NOTION_MAP["posts_per_week"]: {"number": data.get("posts_per_week", 3)},
            CLIENT_NOTION_MAP["briefing_url"]: {"url": data.get("briefing_url")} if data.get("briefing_url") else None,
            CLIENT_NOTION_MAP["brand_manual_url"]: {"url": data.get("brand_manual_url")} if data.get("brand_manual_url") else None,
            CLIENT_NOTION_MAP["plan"]: {"multi_select": [{"name": p} for p in plan]} if plan else None,
            CLIENT_NOTION_MAP["start_date"]: {"date": {"start": data.get("start_date") or data.get("created_at")}} if (data.get("start_date") or data.get("created_at")) else None,
            CLIENT_NOTION_MAP["last_sync"]: {"date": {"start": datetime.now().isoformat()}}
        }
        # Remove None values
        return {k: v for k, v in props.items() if v is not None}
    
    elif entity_type == "content":
        return {
            "Name": {"title": [{"text": {"content": data.get("title", "Untitled Content")}}]},
            "Estado": {"status": {"name": data.get("status", "Borrador")}},
            "👥 Equipo": {"select": {"name": data.get("team", "Team Sofi & Ori")}},
            "🆔 Supabase ID": {"rich_text": [{"text": {"content": str(data.get("id", ""))}}]},
            "🔗 Link": {"url": data.get("url", None)} if data.get("url") else None
        }
    
    return {}
