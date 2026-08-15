import json
from typing import Optional, Dict, Any
from datetime import datetime
from academy.core.models import TrackingEvent, TrackingEventType
from sqlalchemy.orm import Session


def track(
    db: Session,
    event: TrackingEventType,
    user_id: Optional[int] = None,
    course_id: Optional[int] = None,
    enrollment_id: Optional[int] = None,
    payload: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    commit: bool = False,
) -> TrackingEvent:
    obj = TrackingEvent(
        user_id=user_id,
        course_id=course_id,
        enrollment_id=enrollment_id,
        event=event.value,
        payload=json_dumps(payload),
        ip_address=ip_address,
        user_agent=user_agent,
        created_at=datetime.utcnow(),
    )
    db.add(obj)
    if commit:
        db.commit()
        db.refresh(obj)
    return obj


def json_dumps(data: Optional[Dict[str, Any]]) -> Optional[str]:
    if data is None:
        return None
    try:
        return __import__("json").dumps(data, ensure_ascii=False)
    except Exception:
        return str(data)
