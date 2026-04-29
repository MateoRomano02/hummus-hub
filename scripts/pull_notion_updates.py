import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.notion_sync import sync_notion_to_supabase

if __name__ == "__main__":
    print("🚀 Ejecutando Sincronización Validada (Hummus Hub Judge)...")
    result = sync_notion_to_supabase()
    print(f"✅ Finalizado: {result.get('synced')} sincronizados, {result.get('errors')} errores.")
