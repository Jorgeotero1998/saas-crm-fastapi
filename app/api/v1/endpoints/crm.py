from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from app.api.v1.deps import get_current_user, get_db
from app.db.models.crm import Organization, Lead

router = APIRouter()


class OrgCreate(BaseModel):
    name: str


class OrgOut(BaseModel):
    id: str
    name: str


class LeadCreate(BaseModel):
    org_id: str
    email: EmailStr
    name: str
    status: str = "new"


class LeadOut(BaseModel):
    id: str
    org_id: str
    email: EmailStr
    name: str
    status: str


@router.get("/crm/orgs", response_model=list[OrgOut])
async def list_orgs(db=Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Organization))
    rows = result.scalars().all()
    return [OrgOut(id=str(o.id), name=o.name) for o in rows]


@router.post("/crm/orgs", response_model=OrgOut)
async def create_org(payload: OrgCreate, db=Depends(get_db), _=Depends(get_current_user)):
    org = Organization(name=payload.name)
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return OrgOut(id=str(org.id), name=org.name)


@router.get("/crm/leads", response_model=list[LeadOut])
async def list_leads(db=Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Lead))
    rows = result.scalars().all()
    return [
        LeadOut(id=str(l.id), org_id=str(l.org_id), email=l.email, name=l.name, status=l.status)
        for l in rows
    ]


@router.post("/crm/leads", response_model=LeadOut)
async def create_lead(payload: LeadCreate, db=Depends(get_db), _=Depends(get_current_user)):
    lead = Lead(
        org_id=uuid.UUID(payload.org_id),
        email=payload.email,
        name=payload.name,
        status=payload.status,
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return LeadOut(
        id=str(lead.id),
        org_id=str(lead.org_id),
        email=lead.email,
        name=lead.name,
        status=lead.status,
    )

