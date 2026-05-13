from fastapi import FastAPI
from app.routes import upload, ask
from app.routes import agent

app = FastAPI()

app.include_router(upload.router)
app.include_router(ask.router)
app.include_router(agent.router)

@app.get("/")
def home():
    return {"message": "AI Document Assistant Running"}