from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.api.routes_agent import router as agent_router
from app.models.phi3_model import Phi3Model
import uvicorn

# Define the lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("App starting up...")
    settings = get_settings()
    print("Test mode:", settings.test_mode)
    Phi3Model.load(settings.model_id, test_mode=settings.test_mode)  # Load the model once before the app starts serving

    yield
    # Shutdown logic, yields control back to the FastAPI app
    # Everything after yield will run when the app is shutting down
    print("App shutting down...")
    Phi3Model.unload()  # Unload the model and processor from memory

app = FastAPI(lifespan=lifespan)
app.include_router(agent_router, prefix="/api")

if __name__ == "__main__":
    # "app.main:app" is good format ("module:app") in practice, i.e. for reload=True to work properly
    uvicorn.run("app.main:app", host="localhost", port=8000)
