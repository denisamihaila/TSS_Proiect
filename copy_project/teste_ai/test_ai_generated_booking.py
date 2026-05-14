from dataclasses import dataclass
import re

import pytest

from fitness_class_booking import FitnessClassBooking


@dataclass(frozen=True)
class PackageScenario:
    name: str
    history: list[str]
    package_sessions: int
    has_membership: bool
    price: float
    expected: dict


def booking(price: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("yoga", "AI Scenario Instructor", price)


def only(result: dict, keys: tuple[str, ...]) -> dict:
    return {key: result[key] for key in keys}


SCENARIOS = [
    PackageScenario(
        name="cancelled_statuses_are_recorded_but_do_not_consume",
        history=["cancelled", "attended", "cancelled", "no_show", "attended"],
        package_sessions=7,
        has_membership=False,
        price=42.0,
        expected={
            "attended": 2,
            "no_show": 1,
            "cancelled": 2,
            "used_sessions": 3,
            "remaining_sessions": 4,
            "total_cost": 294.0,
            "status": "active",
        },
    ),
    PackageScenario(
        name="clean_completion_tolerates_cancelled_entries",
        history=["cancelled", "attended", "cancelled", "attended"],
        package_sessions=2,
        has_membership=False,
        price=55.0,
        expected={
            "attended": 2,
            "no_show": 0,
            "cancelled": 2,
            "used_sessions": 2,
            "remaining_sessions": 0,
            "total_cost": 110.0,
            "status": "completed_successfully",
        },
    ),
    PackageScenario(
        name="membership_client_with_remaining_sessions",
        history=["no_show", "cancelled", "attended", "no_show"],
        package_sessions=4,
        has_membership=True,
        price=37.5,
        expected={
            "attended": 1,
            "no_show": 2,
            "cancelled": 1,
            "used_sessions": 3,
            "remaining_sessions": 1,
            "total_cost": 120.0,
            "status": "active",
        },
    ),
    PackageScenario(
        name="package_finished_with_at_least_one_absence",
        history=["no_show", "attended", "cancelled", "attended"],
        package_sessions=3,
        has_membership=False,
        price=20.0,
        expected={
            "attended": 2,
            "no_show": 1,
            "cancelled": 1,
            "used_sessions": 3,
            "remaining_sessions": 0,
            "total_cost": 60.0,
            "status": "completed_with_absences",
        },
    ),
    PackageScenario(
        name="unused_large_package_stays_active_with_discounted_price",
        history=[],
        package_sessions=12,
        has_membership=True,
        price=33.33,
        expected={
            "attended": 0,
            "no_show": 0,
            "cancelled": 0,
            "used_sessions": 0,
            "remaining_sessions": 12,
            "total_cost": 319.97,
            "status": "active",
        },
    ),
]


@pytest.mark.parametrize("case", SCENARIOS, ids=lambda case: case.name)
def test_ai_package_scenarios_match_the_business_snapshot(case: PackageScenario) -> None:
    result = booking(case.price).evaluate_client_package(
        case.history,
        case.package_sessions,
        case.has_membership,
    )

    assert only(result, tuple(case.expected)) == case.expected


INVALID_OPERATIONS = [
    pytest.param(
        lambda: FitnessClassBooking("Yoga", "Alex", 30.0),
        "class_name must be dance, pilates, yoga or zumba",
        id="class-name-is-case-sensitive",
    ),
    pytest.param(
        lambda: FitnessClassBooking("dance", " \t\n ", 30.0),
        "instructor must be a non-empty string",
        id="blank-instructor-after-strip",
    ),
    pytest.param(
        lambda: FitnessClassBooking("dance", "Alex", "30"),
        "price_per_session must be greater than 0",
        id="price-is-not-numeric",
    ),
    pytest.param(
        lambda: booking().evaluate_client_package(("attended",), 5, False),
        "invalid package data",
        id="history-is-not-list",
    ),
    pytest.param(
        lambda: booking().evaluate_client_package([], True, False),
        "invalid package data",
        id="package-size-bool-is-rejected",
    ),
    pytest.param(
        lambda: booking().evaluate_client_package([], 5, 0),
        "invalid package data",
        id="membership-must-be-strict-bool",
    ),
    pytest.param(
        lambda: booking().evaluate_client_package(["attended", "rescheduled"], 5, False),
        "invalid session status",
        id="unknown-status-in-history",
    ),
    pytest.param(
        lambda: booking().evaluate_client_package(["attended", "no_show", "attended"], 2, False),
        "used sessions cannot exceed package sessions",
        id="consumed-sessions-over-package",
    ),
]


@pytest.mark.parametrize(("operation", "message"), INVALID_OPERATIONS)
def test_ai_invalid_inputs_fail_with_the_public_error_contract(operation, message) -> None:
    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        operation()
