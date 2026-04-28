import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

print(f"Attributes of notion.data_sources: {dir(notion.data_sources)}")
