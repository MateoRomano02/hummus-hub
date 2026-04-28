import os
from notion_client import Client
from dotenv import load_dotenv
import json

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
database_id = os.getenv("NOTION_DB_CLIENTS")

def inspect_database():
    print(f"Inspecting database: {database_id}")
    try:
        # Try to retrieve DB info
        db = notion.databases.retrieve(database_id=database_id)
        print("\n--- Database Properties (from retrieve) ---")
        for prop_name, prop_info in db.get("properties", {}).items():
            print(f"Property: {prop_name}")
            print(f"  Type: {prop_info['type']}")
            print(f"  ID: {prop_info['id']}")
        
        print("\n--- Sample Query (using data_sources.query) ---")
        # In 3.0.0, query seems to be in data_sources for some reason
        query_res = notion.data_sources.query(data_source_id=database_id, page_size=1)
        
        if query_res["results"]:
            sample_page = query_res["results"][0]
            print(f"Sample Page ID: {sample_page['id']}")
            print("\n--- Page Properties Content ---")
            for p_name, p_val in sample_page["properties"].items():
                print(f"Prop '{p_name}': type={p_val['type']}")
                # print(json.dumps(p_val, indent=2))
        else:
            print("No pages found in database.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    inspect_database()
