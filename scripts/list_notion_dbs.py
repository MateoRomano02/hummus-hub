import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def list_databases():
    print("Listing available databases...")
    try:
        results = notion.search(filter={"value": "database", "property": "object"}).get("results", [])
        for db in results:
            title = db.get("title", [{}])[0].get("plain_text", "Untitled")
            print(f"Database: {title}")
            print(f"  ID: {db['id']}")
            print(f"  URL: {db['url']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_databases()
