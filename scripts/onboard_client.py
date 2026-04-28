import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from database.client import supabase_admin
from notion.sync import push_to_notion
from config.settings import settings

def onboard(data: dict):
    """
    Onboards a new client:
    1. Creates the record in Supabase (Structured Data)
    2. Syncs to Notion (Visual Dashboard)
    """
    name = data.get("name")
    print(f"🚀 Iniciando onboarding para: {name}...")
    
    # 1. Resolve Agency ID
    if not data.get("agency_id"):
        agencies = supabase_admin.table("agencies").select("id").limit(1).execute()
        data["agency_id"] = agencies.data[0]["id"] if agencies.data else settings.default_agency_id
    
    # Generate slug if missing
    if not data.get("slug"):
        data["slug"] = name.lower().replace(" ", "-")
    
    try:
        # 2. Insert into Supabase
        res = supabase_admin.table("clients").insert(data).execute()
        if not res.data:
            print("❌ Error al crear en Supabase")
            return
        
        new_client = res.data[0]
        client_id = new_client["id"]
        print(f"✅ Cliente creado en Supabase (ID: {client_id})")
        
        # 3. Sync to Notion
        notion_id = push_to_notion("client", client_id, new_client)
        
        if notion_id:
            print(f"✨ Dashboard Premium creado en Notion!")
            clean_id = notion_id.replace("-", "")
            print(f"🔗 URL: https://www.notion.so/{clean_id}")
            print("\n💡 Tip: Los pilares estratégicos y archivos se han sincronizado. Ya puedes empezar a trabajar.")
        else:
            print("⚠️ El cliente se creó en la base de datos pero hubo un problema al generar la página de Notion.")
            
    except Exception as e:
        print(f"❌ Error durante el onboarding: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python scripts/onboard_client.py 'Nombre' 'Rubro' 'Equipo' ['URL Briefing'] ['URL Manual']")
        print("Ejemplo: python scripts/onboard_client.py 'Nike' 'Indumentaria' 'Team Sofi & Ori'")
    else:
        # Simple CLI mapping for backwards compatibility
        payload = {
            "name": sys.argv[1],
            "industry": sys.argv[2],
            "assigned_cm": sys.argv[3], # Mapping 'Team' to assigned_cm for now
            "extra": {"onboarded_by": "cli"}
        }
        if len(sys.argv) > 4: payload["extra"]["briefing_url"] = sys.argv[4]
        if len(sys.argv) > 5: payload["brand_manual_url"] = sys.argv[5]
        
        onboard(payload)

