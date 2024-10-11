from fastapi import FastAPI, APIRouter
from routers import items, clock_in


router = APIRouter()

app = FastAPI(title="Vortex API", version="0.1.0")

app.include_router(items.router)
app.include_router(clock_in.router)