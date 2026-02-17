import isodate

def convert_duration(duration_string) -> int:
    return int(isodate.parse_duration(duration_string).total_seconds())
