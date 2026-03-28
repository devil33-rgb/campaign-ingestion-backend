from sqlalchemy import Column, String, Date, Numeric, BigInteger, TIMESTAMP,JSON, text, UniqueConstraint
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


"""
    Campaign model representing normalized ad performance data.

    Fields:
        id (str): Primary key (UUID)
        job_id (str): Identifier linking upload job
        platform (str): Source platform (meta, google, etc.)
        campaign_name (str): Campaign name
        report_date (date): Reporting date

        spend (Decimal): Ad spend
        impressions (int): Total impressions
        clicks (int): Total clicks
        conversions (int): Total conversions
        revenue (Decimal): Revenue generated

        ctr (Decimal): Click-through rate (optional/precomputed)
        roas (Decimal): Return on ad spend (optional/precomputed)

        ad_id (str): Unique ad identifier
        raw_fields (JSONB): Unmapped platform-specific fields

        created_at (timestamp): Record creation time

    Constraints:
        - Unique (platform, ad_id, report_date) ensures idempotency
    """

class Campaign(Base):
    __tablename__ = "campaign_data"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    campaign_name = Column(String, nullable=False)
    report_date = Column(Date, nullable=False)

    spend = Column(Numeric(12,2))
    impressions = Column(BigInteger)
    clicks = Column(BigInteger)
    conversions = Column(BigInteger)
    revenue = Column(Numeric(12,2))

    ctr = Column(Numeric(6,4))
    roas = Column(Numeric(8,4))

    ad_id = Column(String)
    raw_fields = Column(JSON)

    created_at = Column(TIMESTAMP, server_default=text("now()"))

    __table_args__ = (
        UniqueConstraint("platform", "ad_id", "report_date", name="uniq_campaign"),
    )