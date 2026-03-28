from app.jobs.celery_app import celery
from app.ingestion.mapper import map_row
from app.ingestion.validator import validate_row
from app.ingestion.processor import transform
from app.db.session import SessionLocal
from app.db.models import Campaign
from app.jobs.job_model import Job

import csv
from sqlalchemy.dialects.postgresql import insert


@celery.task(bind=True)
def process_csv(self, path, platform, job_id):
    """
    Asynchronous CSV processing task.

    Workflow:
        1. Update job status → processing
        2. Read CSV rows
        3. Map → Validate → Transform
        4. Perform idempotent upsert
        5. Track processed & rejected rows
        6. Mark job complete

    Args:
        path (str): File path in shared volume
        platform (str): Platform identifier
        job_id (str): Job tracking ID
    """
    db = SessionLocal()

    job = db.query(Job).filter(Job.id == job_id).first()
    job.status = "processing"
    db.commit()

    processed = 0
    rejected = 0

    with open(path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                mapped = map_row(row, platform)
                validate_row(mapped)
                final = transform(mapped)
                final.update({"job_id":job_id})
                
                stmt = insert(Campaign).values(**final)

                stmt = stmt.on_conflict_do_update(
                    index_elements=["ad_id", "report_date", "platform"],
                    set_={
                        "campaign_name": stmt.excluded.campaign_name,
                        "spend": stmt.excluded.spend,
                        "revenue": stmt.excluded.revenue,
                        "clicks": stmt.excluded.clicks,
                        "impressions": stmt.excluded.impressions,
                        "raw_fields": stmt.excluded.raw_fields,
                    }
                )

                db.execute(stmt)

                # obj = Campaign(**final,job_id=job_id)
                # db.add(obj)
                db.commit()

                processed += 1

            except Exception:
                rejected += 1

    job.status = "complete"
    job.processed = processed
    job.rejected = rejected

    db.commit()
    db.close()