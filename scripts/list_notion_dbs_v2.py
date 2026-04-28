import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def list_data_sources():
    print("Listing available data sources (databases)...")
    try:
        results = notion.search(filter={"value": "data_source", "property": "object"}).get("results", [])
        for db in results:
            title = db.get("title", [{}])[0].get("plain_text", "Untitled")
            print(f"Data Source: {title}")
            print(f"  ID: {db['id']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_data_sources()
