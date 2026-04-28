from notion_client import Client
from config.settings import settings

notion = Client(auth=settings.notion_api_key)
