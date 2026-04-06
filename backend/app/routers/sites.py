from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services.security import encrypt_secret

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/", response_model=list[schemas.SiteRead])
def list_sites(db: Session = Depends(get_db)):
    return db.query(models.Site).all()


@router.post("/", response_model=schemas.SiteRead)
def create_site(payload: schemas.SiteCreate, db: Session = Depends(get_db)):
    if db.query(models.Site).filter(models.Site.domain == payload.domain).first():
        raise HTTPException(status_code=400, detail="Domain already exists")
    site = models.Site(
        name=payload.name,
        domain=payload.domain,
        username=payload.username,
        app_password_encrypted=encrypt_secret(payload.app_password),
        ux_block_id=payload.ux_block_id,
        notes=payload.notes,
    )
    db.add(site)
    db.commit()
    db.refresh(site)
    return site
