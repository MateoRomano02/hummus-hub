# Roadmap: Hummus Brain

Basado en el documento *Hummus Brain Architecture & Decision Record v3 — Final*.

## Día 1
- **Qué se construye:** Repo GitHub. Estructura de carpetas. `.env.example`. Configurar MCP Notion en Claude Desktop. Con el MCP, pedirle a Claude que cree todas las databases de Notion (Clientes, Tareas, Campañas, Decisiones, Métricas, Assets, Calendario) con todas sus propiedades.
- **Entregable:** Notion operativo con todas las databases creadas.

## Día 2
- **Qué se construye:** Proyecto Supabase. Correr las 13 migraciones SQL en orden. Cliente Python wrapper con `set_agency_context()`. Insertar la primera fila en agencies: `Hummus`.
- **Entregable:** Schema completo en Supabase. RLS habilitado.

## Día 3
- **Qué se construye:** `google_drive.py` con service account setup. POST `/assets/register` funcionando. `sync.py` dirección Supabase→Notion. `load_client.py`. Cargar el cliente demo en ambos sistemas con Cami/Yae.
- **Entregable:** Primer cliente en Notion y Supabase. Demo listo.

## Día 4
- **Qué se construye:** `base_agent.py` con `run_with_retry()` y `prompt_hash`. `brief_agent.py`. `BriefSchema` Pydantic. Endpoint POST `/brief`. `notify_error()` con Gmail SMTP.
- **Entregable:** Primer agente funcional. Error handling operativo.

## Día 5
- **Qué se construye:** Deploy en Railway desde GitHub. POST `/sync/pull/{client_id}` para el sync Notion→Supabase. README completo. Demo final con Cami y Yae.
- **Entregable:** Sistema en producción. Demo funcionando.
