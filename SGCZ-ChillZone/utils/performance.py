import time, threading

_lock = threading.Lock()
_last_durations: list[float] = []
_MAX = 200

def record(duration_ms: float):
    with _lock:
        _last_durations.append(duration_ms)
        if len(_last_durations) > _MAX:
            del _last_durations[0:len(_last_durations)-_MAX]

def avg_ms() -> float:
    with _lock:
        if not _last_durations:
            return 0.0
        return sum(_last_durations) / len(_last_durations)
