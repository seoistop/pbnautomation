from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine
from .routers import sites, tasks

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_token(authorization: str | None = Header(default=None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    scheme, _, token = authorization.partition(" ")
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")


@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}


app.include_router(sites.router, dependencies=[Depends(verify_token)])
app.include_router(tasks.router, dependencies=[Depends(verify_token)])
