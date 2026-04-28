import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DB_CLIENTS_ID = os.getenv("NOTION_DB_CLIENTS")
DB_CONTENT_ID = os.getenv("NOTION_DB_CONTENT")

def get_page_id_by_title(title):
    results = notion.search(query=title, filter={"property": "object", "value": "page"}).get("results")
    for res in results:
        # Check title
        props = res.get("properties", {})
        title_list = props.get("title", {}).get("title", [])
        if not title_list:
            # Maybe it's a database or has a different title property name
            continue
        if title_list[0].get("plain_text") == title:
            return res["id"]
    return None

def setup_team_page(page_id, team_name):
    print(f"Setting up dashboard for {team_name}...")
    
    # Blocks to add
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📊 STATUS EQUIPO (Trello Style)"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"Esta vista muestra todas las tareas de {team_name} agrupadas por estado."}}]}
        },
        # Notion API doesn't support creating "Linked Views" of databases with specific filters/groupings via the block API easily.
        # It creates a 'child_database' which is a NEW database.
        # To create a 'Linked View' (synced database), the API is limited.
        # However, we can add a callout with a link or instructions.
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "💡 Acción requerida: Haz clic en /linked para vincular la base de 'Content' y fíltrala por este equipo."}}],
                "icon": {"type": "emoji", "emoji": "🚀"}
            }
        }
    ]
    
    notion.blocks.children.append(block_id=page_id, children=children)

def main():
    teams = ["Team Sofi & Ori", "Team Flor & Angie"]
    for team in teams:
        id = get_page_id_by_title(team)
        if id:
            setup_team_page(id, team)
        else:
            print(f"Could not find page for {team}")

if __name__ == "__main__":
    main()
