import pytest
from pytest_bdd import given, scenarios, then, when


pytestmark = pytest.mark.bdd

scenarios("health.feature")


@pytest.fixture
def context():
    return {}


@given("the backend is running")
def backend_is_running(client, context):
    context["client"] = client


@when("I request the health endpoint")
def request_health(context):
    response = context["client"].get("/health")
    context["response"] = response


@then("I receive an ok status")
def check_status(context):
    response = context["response"]
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
