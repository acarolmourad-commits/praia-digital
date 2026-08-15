"""Migration to add tracking, content source, and admin features."""
from sqlalchemy import text
from academy.core.database import engine, Base
from academy.core.models_tracking import (
    TrackingEvent,
    CourseContentSource,
    TrackingEventType,
    ContentSourceType,
)
from academy.core.models import (
    User,
    Course,
    Enrollment,
    Payment,
    Order,
    Module,
    Lesson,
    ContentAttachment,
    Certificate,
)


def migrate():
    tables = [
        TrackingEvent.__table__,
        CourseContentSource.__table__,
    ]
    for table in tables:
        try:
            table.create(bind=engine, checkfirst=True)
            print(f"table ready: {table.name}")
        except Exception as exc:
            print(f"table error {table.name}: {exc}")
    print("migration complete")


if __name__ == "__main__":
    migrate()
