from datetime import datetime

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
            "Name": {"title": [{"text": {"content": data.get("name", "Unknown")}}]},
            "📝 Descripción": {"rich_text": [{"text": {"content": data.get("description", "") or ""}}]},
            "📋 Rubro": {"select": {"name": data.get("industry", "Servicios") or "Servicios"}},
            "👥 Equipo": {"select": {"name": data.get("team", "Team Sofi & Ori") or "Team Sofi & Ori"}},
            "🆔 Supabase ID": {"rich_text": [{"text": {"content": str(data.get("id", ""))}}]},
            "🗣️ Tono de Voz": {"rich_text": [{"text": {"content": data.get("brand_voice", "") or ""}}]},
            "🎯 Público Objetivo": {"rich_text": [{"text": {"content": data.get("target_audience", "") or ""}}]},
            "💎 Propuesta de Valor": {"rich_text": [{"text": {"content": data.get("value_prop", "") or ""}}]},
            "🥊 Competencia": {"rich_text": [{"text": {"content": data.get("competition", "") or ""}}]},
            "💡 Estrategia": {"rich_text": [{"text": {"content": data.get("strategy", "") or ""}}]},
            "📂 Briefing": {"url": data.get("briefing_url")} if data.get("briefing_url") else None,
            "🔗 Manual de Marca": {"url": data.get("brand_manual_url")} if data.get("brand_manual_url") else None,
            "📈 Plan": {"multi_select": [{"name": p} for p in plan]} if plan else None,
            "📅 Comienzo": {"date": {"start": data.get("start_date") or data.get("created_at")}} if (data.get("start_date") or data.get("created_at")) else None,
            "⌛ Last Sync": {"date": {"start": datetime.now().isoformat()}}
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
