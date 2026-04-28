import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from notion.client import notion
from notion.blocks import build_dashboard_blocks, build_team_page_blocks
from config.settings import settings

def create_dashboard():
    print("🚀 Iniciando creación del Master Dashboard...")
    
    # 1. Create Master Dashboard
    dashboard_parent = {"page_id": settings.notion_page_id}
    dashboard_blocks = build_dashboard_blocks()
    
    dashboard_page = notion.pages.create(
        parent=dashboard_parent,
        properties={
            "title": {
                "title": [{"type": "text", "text": {"content": "🏛️ Hummus Hub Master Dashboard"}}]
            }
        },
        children=dashboard_blocks
    )
    
    dashboard_id = dashboard_page["id"]
    print(f"✅ Dashboard Creado: {dashboard_id}")
    
    # 2. Create Team Pages
    teams = ["Sofi & Ori", "Flor & Angie"]
    team_links = []
    
    for team in teams:
        print(f"📦 Creando espacio para equipo: {team}...")
        team_blocks = build_team_page_blocks(team)
        team_page = notion.pages.create(
            parent={"page_id": dashboard_id},
            properties={
                "title": {
                    "title": [{"type": "text", "text": {"content": f"⚡ Workspace: {team}"}}]
                }
            },
            children=team_blocks
        )
        team_links.append((team, team_page["id"]))
        print(f"✅ Espacio {team} creado.")

    # 3. Add links to Team Pages in the Master Dashboard
    # We find the 'Espacios de Equipo' heading and append after it
    # For simplicity, we just append to the end of the page for now
    link_blocks = [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "🔗 Accesos Directos"}}]
            }
        }
    ]
    
    for name, page_id in team_links:
        link_blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"👉 Ir al espacio de {name}",
                            "link": {"url": f"https://www.notion.so/{page_id.replace('-', '')}"}
                        }
                    }
                ]
            }
        })
        
    notion.blocks.children.append(dashboard_id, children=link_blocks)
    print("✨ Dashboard configurado con éxito.")

if __name__ == "__main__":
    if not settings.notion_page_id:
        print("❌ Error: NOTION_PAGE_ID no configurada en .env")
        sys.exit(1)
    create_dashboard()
