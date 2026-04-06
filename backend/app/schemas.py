from datetime import datetime

from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    name: str
    domain: str
    username: str
    ux_block_id: int
    notes: str | None = None


class SiteCreate(SiteBase):
    app_password: str = Field(..., min_length=8)


class SiteRead(SiteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    site_id: int
    url: str
    anchor_text: str
    html_wrapper_before: str | None = None
    html_wrapper_after: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    status: str
    log: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskTriggerRequest(BaseModel):
    task_id: int


class AnchorPayload(BaseModel):
    url: str
    anchor_text: str
    site_id: int
    html_wrapper_before: str | None = None
    html_wrapper_after: str | None = None
