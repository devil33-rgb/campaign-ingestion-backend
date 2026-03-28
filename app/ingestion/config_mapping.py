#Platform wise common schema mapper logic
PLATFORM_MAPPING = {
    "meta": {
        "campaign_name": "campaign_name",
        "report_date": "date",
        "spend": "amount_spent",
        "impressions": "impressions",
        "clicks": "link_clicks",
        "conversions": "purchases",
        "revenue": "purchase_value",
        "ad_id": "ad_id"
    },
    "google": {
        "campaign_name": "campaign",
        "report_date": "day",
        "spend": "cost",
        "impressions": "impressions",
        "clicks": "clicks",
        "conversions": "conversions",
        "revenue": "conversion_value",
        "ad_id": "ad_id"
    },
    "flipkart": {
        "campaign_name": "campaign_title",
        "report_date": "report_date",
        "spend": "spend",
        "impressions": "total_impressions",
        "clicks": "ad_clicks",
        "conversions": "orders",
        "revenue": "gmv",
        "ad_id": "creative_id"
    }
}