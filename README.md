# Hummus Brain

Sistema central de inteligencia artificial y gestión para Agencia Hummus.
Construido usando FastAPI, Supabase, Notion y Claude (Haiku).

## Arquitectura

- **Fuente de verdad:** Supabase (PostgreSQL) con Row Level Security (RLS) para multi-tenant.
- **Interfaz (UI):** Notion (conectado asincrónicamente al backend).
- **Almacenamiento de archivos:** Google Drive (referenciado en DB).
- **Agentes AI:** Claude Haiku (Anthropic API).
- **Backend:** FastAPI expone las APIs e interfaces.

## Requisitos Previos

- Python 3.10+
- Entorno virtual (venv)
- Archivo `.env` configurado (ver `.env.example`)

## Instalación Local

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor local
uvicorn api.main:app --reload
```

## Sincronización y Configuración

El proyecto cuenta con scripts de inicialización en la carpeta `/scripts`:
- `setup_notion.py`: Crea las bases de datos iniciales en Notion.
- `load_client.py`: Carga el primer cliente.
- `backfill.py`: Para migrar clientes existentes.

Las migraciones de Supabase están en `supabase/migrations/` numeradas secuencialmente del 001 al 013.
