from fastapi import FastAPI
from api.routes import brief, assets, sync, clients, intake, agents
from apscheduler.schedulers.background import BackgroundScheduler
from integrations.notion_sync import sync_notion_to_supabase
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hummus Brain API", version="3.0.0")

# Setup Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(sync_notion_to_supabase, 'interval', minutes=5)

@app.on_event("startup")
def startup_event():
    logger.info("Starting background scheduler...")
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down background scheduler...")
    scheduler.shutdown()

app.include_router(brief.router, prefix="/brief", tags=["Brief"])
app.include_router(assets.router, prefix="/assets", tags=["Assets"])
app.include_router(sync.router, prefix="/sync", tags=["Sync"])
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(intake.router, prefix="/intake", tags=["Intake"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])

@app.get("/")
def read_root():
    return {"status": "ok", "system": "Hummus Brain v3", "scheduler": "active"}
