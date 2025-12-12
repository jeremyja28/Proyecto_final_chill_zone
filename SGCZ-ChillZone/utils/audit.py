import json, os, datetime
from flask import session, request

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'audit.log')

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def audit_log(event: str, subject: str, entity_id: int | None = None, details: dict | None = None):
    """Registra una línea de auditoría en logs/audit.log.
    Campos: timestamp, user_id, rol, ip, event, subject, entity_id, details_json
    No lanza excepciones para no romper el flujo principal.
    """
    try:
        record = {
            'ts': datetime.datetime.utcnow().isoformat(timespec='seconds')+'Z',
            'user_id': session.get('user_id'),
            'rol': session.get('rol'),
            'ip': request.remote_addr,
            'event': event,
            'subject': subject,
            'entity_id': entity_id,
            'details': details or {}
        }
        line = json.dumps(record, ensure_ascii=False)
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass
