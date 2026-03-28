def validate_row(row):
    for field in ["campaign_name", "report_date", "spend"]:
        if not row.get(field):
            raise ValueError(f"{field} missing")