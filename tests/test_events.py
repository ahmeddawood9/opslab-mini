from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.events import create_event, get_event, list_events
from app.db.database import Base
from app.schemas.events import EventCreate

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)


def get_test_db():
    db = TestingSessionLocal()
    try:
        return db
    finally:
        pass


def test_create_and_get_event():
    db = get_test_db()
    payload = EventCreate(
        service_name="payments-api",
        event_type="DEPLOYMENT",
        environment="dev",
        message="Deployed version 1.2.3",
    )

    created = create_event(payload, db)

    assert created.id
    assert created.service_name == payload.service_name
    assert created.event_type == payload.event_type

    found = get_event(created.id, db)

    assert found.id == created.id
    db.close()


def test_list_events_with_pagination():
    db = get_test_db()
    events = list_events(limit=10, offset=0, db=db)

    assert isinstance(events, list)
    db.close()
