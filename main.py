from fastapi import FastAPI
from database.models import Base
from database.session import engine
from routers.projects import router as projects_router
from routers.places import router as places_router

app = FastAPI(title="Travel_Planner")

Base.metadata.create_all(bind=engine)

app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(places_router, prefix="/projects", tags=["Places"])