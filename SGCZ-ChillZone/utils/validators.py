import re
from datetime import datetime, time

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email or ''))


def parse_time_str(hhmm: str) -> time:
    return datetime.strptime(hhmm, '%H:%M').time()


def time_overlap(start_a: time, end_a: time, start_b: time, end_b: time) -> bool:
    return max(start_a, start_b) < min(end_a, end_b)


def validate_slot(start: time, end: time) -> bool:
    return start < end
