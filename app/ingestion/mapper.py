from app.ingestion.config_mapping import PLATFORM_MAPPING

def map_row(row, platform):
    """
    Map a raw CSV row into a normalized campaign schema.

    Args:
        row (Dict[str, Any]): Raw CSV row as dictionary
        platform (str): Platform identifier (meta, google, etc.)

    Returns:
        Dict[str, Any]: Normalized data with:
            - mapped fields based on PLATFORM_MAPPING
            - raw_fields containing unmapped columns
            - platform field added

    Raises:
        ValueError: If platform mapping is not defined

    Notes:
        - Ensures flexibility by storing unmapped fields in JSON (raw_fields)
        - Missing values are kept as None
    """
    mapping = PLATFORM_MAPPING[platform]

    mapped = {}
    raw_fields = {}

    for target, source in mapping.items():
        mapped[target] = row.get(source)

    for key in row:
        if key not in mapping.values():
            raw_fields[key] = row[key]

    mapped["raw_fields"] = raw_fields
    mapped["platform"] = platform

    return mapped