from datetime import datetime, timezone



# Returns the current UTC datetime for consistent backend time handling.
def utc_now() -> datetime:
    return datetime.now(timezone.utc)
