import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DB_CLIENTS")

def check_clients():
    try:
        res = notion.data_sources.query(data_source_id=database_id)
        results = res.get("results", [])
        print(f"Total clients in Notion: {len(results)}")
        for page in results:
            name = page["properties"]["Name"]["title"][0]["plain_text"]
            trigger = page["properties"]["🔄 Sync Trigger"]["checkbox"]
            print(f"- {name}: Sync Trigger={trigger}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_clients()
