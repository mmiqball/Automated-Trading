from datetime import datetime, timedelta

def format_number(current, match):
    """
        Returns a string with the current number's 
        desired number of decimals
    """
    current_str = f"{current}"
    match_str = f"{match}"
    if "." in match_str:
        match_decimals = len(match_str.split(".")[1])
        current_str = f"{current:.{match_decimals}f}"
        current_str = current_str[:]
        return current_str
    else:
        return f"{int(current)}"

def format_time(timestamp):
    return timestamp.replace(microsecond=0).isoformat()

def get_times():
    date_start = datetime.now()
    date_start1 = date_start - timedelta(hours=100)
    date_start2 = date_start1 - timedelta(hours=100)
    date_start3 = date_start2 - timedelta(hours=100)
    date_start4 = date_start3 - timedelta(hours=100)
    times_dict = {
        "range1": {
            "from_iso": format_time(date_start1),
            "to_iso": format_time(date_start)
        }, 
        "range2": {
            "from_iso": format_time(date_start2),
            "to_iso": format_time(date_start1)
        },
        "range3": {
            "from_iso": format_time(date_start3),
            "to_iso": format_time(date_start2)
        },
        "range4": {
            "from_iso": format_time(date_start4),
            "to_iso": format_time(date_start3)
        }
    }
    return times_dict