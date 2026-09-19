from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import auth, spaces, recommendations, market, growing

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rootline API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(spaces.router)
app.include_router(recommendations.router)
app.include_router(market.router)
app.include_router(growing.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "rootline-api"}
