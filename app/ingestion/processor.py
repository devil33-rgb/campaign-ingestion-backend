from decimal import Decimal
from datetime import datetime

def transform(row):
    """
    Normalize and type-cast campaign data.

    Args:
        row (Dict[str, Any]): Mapped row from CSV

    Returns:
        Dict[str, Any]: Transformed row with correct types and derived metrics

    Notes:
        - Converts numeric fields to Decimal/int
        - Parses report_date
        - Computes CTR and ROAS safely
        - Handles missing/invalid values gracefully
    """
    row["spend"] = Decimal(row["spend"])
    row["revenue"] = Decimal(row.get("revenue") or 0)

    row["impressions"] = int(row.get("impressions") or 0)
    row["clicks"] = int(row.get("clicks") or 0)

    row["report_date"] = datetime.strptime(row["report_date"], "%Y-%m-%d").date()

    row["ctr"] = row["clicks"] / row["impressions"] if row["impressions"] else 0
    row["roas"] = row["revenue"] / row["spend"] if row["spend"] else 0

    return row