from fastapi import APIRouter, UploadFile, File
import uuid

from app.jobs.tasks import process_csv
from app.db.session import SessionLocal
from app.jobs.job_model import Job
from app.db.models import Campaign
from app.schemas.campaign import CampaignResponse
from app.schemas.platforms import PlatformEnum
from sqlalchemy import func

router = APIRouter()

@router.post("/upload/{platform}")
async def upload_csv(platform: PlatformEnum, file: UploadFile = File(...)):
    """
    Upload a CSV file for a specific advertising platform.

    Args:
        platform (PlatformEnum): Platform name (meta, google, etc.)
        file (UploadFile): CSV file to upload

    Returns:
        dict:
            - job_id (str): Unique identifier to track processing status

    Workflow:
        1. Save file to shared volume
        2. Create job entry in DB
        3. Trigger async Celery task
    """
    job_id = str(uuid.uuid4())

    path = f"/shared/{job_id}.csv"
    with open(path, "wb") as f:
        f.write(await file.read())

    db = SessionLocal()
    db.add(Job(id=job_id))
    db.commit()
    db.close()

    process_csv.delay(path, platform, job_id)

    return {"job_id": job_id}


@router.get("/jobs/{job_id}")
def get_job(job_id: str):
    """
    Fetch job status using job_id.

    Args:
        job_id (str): Unique job identifier

    Returns:
        Job: Job record from database (status, timestamps, etc.)
    """
    db = SessionLocal()
    job = db.query(Job).filter(Job.id == job_id).first()
    db.close()

    return job


@router.get("/campaigns",response_model=list[CampaignResponse])
def get_campaigns():
    """
    Fetch aggregated campaign performance across all ads.

    Returns:
        List[CampaignResponse]:
            - ad_id
            - campaign_name
            - total_spend
            - total_revenue

    Notes:
        - Aggregation is grouped by (ad_id, campaign_name)
        - Prevents duplicate entries
    """
    db = SessionLocal()

    data = db.query(
        Campaign.ad_id,
        Campaign.campaign_name,
        func.sum(Campaign.spend).label("total_spend"),
        func.sum(Campaign.revenue).label("total_revenue")
    ).group_by(Campaign.ad_id,Campaign.campaign_name).all()

    db.close()
    return data


@router.get("/campaigns/{ad_id}", response_model=list[CampaignResponse])
def get_campaigns_by_job(ad_id: str):
    """
    Fetch aggregated campaign performance for a specific ad_id.

    Args:
        ad_id (str): Ad identifier

    Returns:
        List[CampaignResponse]:
            Aggregated campaign metrics filtered by ad_id
    """
    db = SessionLocal()

    results = db.query(
        Campaign.ad_id,
        Campaign.campaign_name,
        func.sum(Campaign.spend).label("total_spend"),
        func.sum(Campaign.revenue).label("total_revenue")
    ).filter(
        Campaign.ad_id == ad_id
    ).group_by(Campaign.ad_id,
        Campaign.campaign_name
    ).all()

    db.close()

    # 🔥 convert properly
    return [
        {
            "ad_id":ad_id,
            "campaign_name": r.campaign_name,
            "total_spend": float(r.total_spend or 0),
            "total_revenue": float(r.total_revenue or 0),
        }
        for r in results
    ]