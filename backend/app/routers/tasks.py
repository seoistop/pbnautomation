from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services.wordpress import WordPressClient

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).order_by(models.Task.created_at.desc()).all()


@router.post("/", response_model=schemas.TaskRead)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    site = db.query(models.Site).filter(models.Site.id == payload.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.post("/trigger", response_model=schemas.TaskRead)
def trigger_task(payload: schemas.TaskTriggerRequest, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == payload.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    site = db.query(models.Site).filter(models.Site.id == task.site_id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    client = WordPressClient(site.domain, site.username, site.app_password_encrypted, site.ux_block_id)

    try:
        client.append_anchor(
            url=task.url,
            anchor_text=task.anchor_text,
            before=task.html_wrapper_before,
            after=task.html_wrapper_after,
        )
        task.status = "completed"
        task.log = "Anchor injected successfully"
    except Exception as exc:  # noqa: BLE001
        task.status = "failed"
        task.log = str(exc)
        db.commit()
        db.refresh(task)
        raise HTTPException(status_code=500, detail=f"Failed to inject anchor: {exc}") from exc

    db.commit()
    db.refresh(task)
    return task
