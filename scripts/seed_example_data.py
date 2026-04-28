import uuid
from datetime import datetime
from notion.sync import push_to_notion
from database.client import supabase_admin
from config.settings import settings

def seed_example_client():
    """
    Crea un cliente de ejemplo 'premium' con toda la data del Second Brain
    para demostrar cómo se ve la arquitectura.
    """
    
    # 1. Definir la data del cliente (Basado en BriefSchema)
    agency_id = "5ce171c4-3826-48e2-b1d5-4d91f6dbe335" # ID de Hummus Hub
    
    client_data = {
        "agency_id": agency_id,
        "name": "Granos & Co. (Premium)",
        "slug": "granos-y-co-premium",
        "industry": "Gastronomía",
        "team": "Team Sofi & Ori",
        "brand_voice": "Cercano, experto, minimalista y auténtico. Evita el lenguaje corporativo.",
        "target_audience": "Amantes del café de especialidad de 25 a 45 años que valoran la trazabilidad y la estética.",
        "value_prop": "Café de especialidad tostado en Buenos Aires con impacto social directo en origen.",
        "dos": ["Usar fotos de alta calidad con luz natural", "Mencionar el origen del grano", "Responder comentarios con emojis de café"],
        "donts": ["Usar stock photos genéricas", "Publicar flyers con mucho texto", "Hablar de 'precios' de forma fría"],
        "brand_colors": ["#4B3621", "#D2B48C", "#F5F5DC"],
        "fonts": ["Playfair Display", "Montserrat"],
        "start_date": "2024-05-01",
        "extra": {
            "five_brand_words": ["Auténtico", "Artesanal", "Minimalista", "Experto", "Sustentable"],
            "plan": ["Redes Sociales", "Estrategia IA"]
        }
    }

    print(f"--- Seeding Example Client: {client_data['name']} ---")

    # 2. Insertar en Supabase
    res = supabase_admin.table("clients").upsert(client_data, on_conflict="slug").execute()
    if not res.data:
        print("Error seeding to Supabase")
        return
    
    db_client = res.data[0]
    client_id = db_client["id"]
    print(f"Supabase Client ID: {client_id}")

    # 3. Empujar a Notion
    # push_to_notion maneja la creación de la página y la actualización de las propiedades
    notion_id = push_to_notion("client", client_id, db_client)
    
    if notion_id:
        print(f"Notion Page Created/Updated: {notion_id}")
        
        # 4. (Opcional) Agregar bloques de contenido a la página de Notion para el "Second Brain" visual
        # Esto lo haremos en una segunda fase del sync.py para que sea automático.
    else:
        print("Error pushing to Notion")

if __name__ == "__main__":
    seed_example_client()
