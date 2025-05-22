import pytest
from dotenv import load_dotenv

from mail.mail_action import Mail


@pytest.fixture(scope="session")
def mail_client():
    return Mail()

@pytest.fixture(autouse=True)
def dotenv():
    return load_dotenv()
