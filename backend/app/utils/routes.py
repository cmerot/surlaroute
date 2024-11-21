from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.core.db.session import SessionDep
from app.core.email.utils import generate_test_email, send_email
from app.core.security import get_current_active_superuser
from app.utils.schemas import Message
from tests.directory.fixtures import (
    activity_fixtures,
    om_fixtures,
    organisation_fixtures,
    person_fixtures,
)

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True


@router.get("/load-fixtures")
def load_fixtures(session: SessionDep) -> Any:
    session.add_all(activity_fixtures)
    session.add_all(organisation_fixtures)
    session.add_all(person_fixtures)
    session.add_all(om_fixtures)
    session.commit()
    return {"message": "Fixtures loaded"}
