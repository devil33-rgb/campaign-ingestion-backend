from pydantic import BaseModel
from datetime import date

class CampaignResponse(BaseModel):
    """
    Response schema for aggregated campaign data.

    Fields:
        ad_id (str): Unique ad identifier
        campaign_name (str): Campaign name
        total_spend (float): Aggregated spend
        total_revenue (float): Aggregated revenue
    """
    campaign_name: str
    total_spend: float
    total_revenue: float
    ad_id: str

class JobResponse(BaseModel):
    """
    Response schema for JobResponse data.

    Fields:
        id (str): Unique ad identifier
        status (str): Status of Job
        processed (int): Processed or not
        rejected (rejected): Is rejected or not
    """
    id: str
    status: str
    processed: int
    rejected: int
    