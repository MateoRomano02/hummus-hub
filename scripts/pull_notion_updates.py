import os
from notion_client import Client
from database.client import supabase_admin
from config.settings import settings
from datetime import datetime

notion = Client(auth=settings.notion_token)

def parse_notion_property(prop):
    """
    Parses a Notion property based on its type to get a plain string or value.
    """
    p_type = prop.get("type")
    if p_type == "rich_text":
        return "".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
    elif p_type == "title":
        return "".join([t.get("plain_text", "") for t in prop.get("title", [])])
    elif p_type == "select":
        return prop.get("select", {}).get("name") if prop.get("select") else None
    elif p_type == "multi_select":
        return [s.get("name") for s in prop.get("multi_select", [])]
    elif p_type == "url":
        return prop.get("url")
    elif p_type == "date":
        return prop.get("date", {}).get("start") if prop.get("date") else None
    return None

def pull_updates():
    print(f"🔍 Escaneando Notion para detectar cambios estratégicos...")
    
    # 1. Obtener todos los clientes de la DB de Notion
    results = notion.databases.query(database_id=settings.notion_db_clients).get("results")
    
    updates_count = 0
    for page in results:
        props = page.get("properties", {})
        
        # Extraer ID de Supabase (nuestra ancla)
        supabase_id = parse_notion_property(props.get("🆔 Supabase ID"))
        if not supabase_id:
            continue
            
        # Extraer campos estratégicos que las chicas pueden editar
        strategic_data = {
            "name": parse_notion_property(props.get("Name")),
            "brand_voice": parse_notion_property(props.get("🗣️ Tono de Voz")),
            "target_audience": parse_notion_property(props.get("🎯 Público Objetivo")),
            "value_prop": parse_notion_property(props.get("💎 Propuesta de Valor")),
            "competition": parse_notion_property(props.get("🥊 Competencia")),
            "strategy": parse_notion_property(props.get("💡 Estrategia")),
            "industry": parse_notion_property(props.get("📋 Rubro")),
            "team": parse_notion_property(props.get("👥 Equipo")),
            "briefing_url": parse_notion_property(props.get("📂 Briefing")),
            "brand_manual_url": parse_notion_property(props.get("🔗 Manual de Marca"))
        }
        
        # Limpiar valores Nones
        strategic_data = {k: v for k, v in strategic_data.items() if v is not None}
        
        # 2. Actualizar Supabase
        # Solo actualizamos si hay algo que actualizar
        if strategic_data:
            print(f"🔄 Sincronizando: {strategic_data['name']}...")
            try:
                supabase_admin.table("clients").update(strategic_data).eq("id", supabase_id).execute()
                updates_count += 1
            except Exception as e:
                print(f"❌ Error actualizando {strategic_data['name']}: {str(e)}")
                
    print(f"✅ Sincronización finalizada. {updates_count} clientes actualizados en el 'Cerebro' (Supabase).")

if __name__ == "__main__":
    pull_updates()
