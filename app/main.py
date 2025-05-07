from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn server
    uvicorn.run(app, host="localhost", port=8000)
