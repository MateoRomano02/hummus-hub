import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HUB_PAGE_ID = "350aa2e860408058891fea1f3a4a72de"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def move_page(page_id, parent_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {
        "parent": {"page_id": parent_id}
    }
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

def append_blocks(block_id, children):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    data = {"children": children}
    response = requests.patch(url, headers=headers, json=data)
    return response.json()

def delete_block(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    response = requests.delete(url, headers=headers)
    return response.json()

def get_children(block_id):
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    response = requests.get(url, headers=headers)
    return response.json().get("results", [])

# IDs from investigation
TEAM_PAGES = {
    "Team Sofi & Ori": "350aa2e8-6040-81e6-92b9-c41c78fb6188",
    "Team Flor & Angie": "350aa2e8-6040-8153-a4a3-faac4d603aaf",
    "Team Caro": "350aa2e8-6040-81bf-9f43-f35a9d26a340"
}

def run():
    print("Moving team pages to Hub level for sidebar visibility...")
    for name, tid in TEAM_PAGES.items():
        move_page(tid, HUB_PAGE_ID)
        print(f"Moved {name}")

    # Delete the now redundant folder if it exists
    # delete_block("350aa2e8-6040-81a9-91b3-f5b2f86e89f1")

    # Build the Dashboard
    dashboard_blocks = [
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Hummus Agency OS"}}]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "👥 Equipos de Trabajo"}}]
            }
        },
        {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {
                                    "object": "block",
                                    "type": "callout",
                                    "callout": {
                                        "rich_text": [{"type": "text", "text": {"content": "Team Sofi & Ori"}}],
                                        "icon": {"type": "emoji", "emoji": "👭"},
                                        "color": "blue_background"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {
                                    "object": "block",
                                    "type": "callout",
                                    "callout": {
                                        "rich_text": [{"type": "text", "text": {"content": "Team Flor & Angie"}}],
                                        "icon": {"type": "emoji", "emoji": "✨"},
                                        "color": "purple_background"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {
                                    "object": "block",
                                    "type": "callout",
                                    "callout": {
                                        "rich_text": [{"type": "text", "text": {"content": "Team Caro"}}],
                                        "icon": {"type": "emoji", "emoji": "👩"},
                                        "color": "orange_background"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📂 Bases de Datos Maestro"}}]
            }
        },
        {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "Maestro Clientes"}}], "icon": {"type": "emoji", "emoji": "🏢"}, "color": "gray_background"}},
                                {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "Maestro Contenido"}}], "icon": {"type": "emoji", "emoji": "✍️"}, "color": "gray_background"}}
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "Calendario Editorial"}}], "icon": {"type": "emoji", "emoji": "📅"}, "color": "gray_background"}},
                                {"object": "block", "type": "callout", "callout": {"rich_text": [{"type": "text", "text": {"content": "Repositorio Assets"}}], "icon": {"type": "emoji", "emoji": "🖼"}, "color": "gray_background"}}
                            ]
                        }
                    }
                ]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🛠 Soporte y Recursos"}}]
            }
        },
        {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "🔐 Gestión de Accesos"}}]}},
                                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "🎨 Guías de Edición"}}]}}
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "column",
                        "column": {
                            "children": [
                                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "📢 Estrategia Influencers"}}]}},
                                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": "🔥 Protocolo HOT SALE"}}]}}
                            ]
                        }
                    }
                ]
            }
        }
    ]

    print("Creating layout structure...")
    res = append_blocks(HUB_PAGE_ID, dashboard_blocks)
    if "results" not in res:
        print(f"Error creating layout: {res}")
        return

    print("Dashboard creation complete.")

if __name__ == "__main__":
    run()
