import re

import pytest

from fitness_class_booking import FitnessClassBooking


def trainer(class_name: str = "pilates", price: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking(class_name, "  Ioana AI  ", price)


def expect_value_error(operation, message: str) -> None:
    with pytest.raises(ValueError, match=f"^{re.escape(message)}$"):
        operation()


@pytest.mark.parametrize(
    ("class_name", "raw_instructor", "price", "normalized_instructor"),
    [
        pytest.param("dance", "   Dana   ", 25, "Dana", id="valid-dance-int-price"),
        pytest.param("pilates", "\tMara\n", 31.5, "Mara", id="valid-pilates-float-price"),
        pytest.param("yoga", "Andrei", 1, "Andrei", id="valid-yoga-minimal-price"),
        pytest.param("zumba", "Elena AI", 99.99, "Elena AI", id="valid-zumba-decimal-price"),
    ],
)
def test_ai_constructor_valid_equivalence_groups_normalize_state(
    class_name,
    raw_instructor,
    price,
    normalized_instructor,
) -> None:
    booking = FitnessClassBooking(class_name, raw_instructor, price)

    assert (booking.class_name, booking.instructor, booking.price_per_session) == (
        class_name,
        normalized_instructor,
        float(price),
    )


@pytest.mark.parametrize(
    ("operation", "message"),
    [
        pytest.param(
            lambda: FitnessClassBooking(None, "Ana", 10),
            "class_name must be dance, pilates, yoga or zumba",
            id="class-name-none",
        ),
        pytest.param(
            lambda: FitnessClassBooking("cycling", "Ana", 10),
            "class_name must be dance, pilates, yoga or zumba",
            id="class-name-outside-domain",
        ),
        pytest.param(
            lambda: FitnessClassBooking("yoga", [], 10),
            "instructor must be a non-empty string",
            id="instructor-not-text",
        ),
        pytest.param(
            lambda: FitnessClassBooking("yoga", "", 10),
            "instructor must be a non-empty string",
            id="instructor-empty",
        ),
        pytest.param(
            lambda: FitnessClassBooking("yoga", "Ana", False),
            "price_per_session must be greater than 0",
            id="price-bool",
        ),
        pytest.param(
            lambda: FitnessClassBooking("yoga", "Ana", -0.01),
            "price_per_session must be greater than 0",
            id="price-negative",
        ),
    ],
)
def test_ai_constructor_invalid_equivalence_groups_keep_distinct_messages(
    operation,
    message,
) -> None:
    expect_value_error(operation, message)


@pytest.mark.parametrize(
    ("label", "history", "package_sessions", "member", "expected"),
    [
        pytest.param(
            "empty-history",
            [],
            9,
            False,
            {"used_sessions": 0, "remaining_sessions": 9, "status": "active"},
            id="valid-empty-history",
        ),
        pytest.param(
            "only-cancellations",
            ["cancelled", "cancelled"],
            4,
            True,
            {
                "cancelled": 2,
                "used_sessions": 0,
                "remaining_sessions": 4,
                "total_cost": 160.0,
                "status": "active",
            },
            id="valid-cancelled-only",
        ),
        pytest.param(
            "mixed-active",
            ["attended", "cancelled", "no_show", "attended"],
            7,
            False,
            {"attended": 2, "no_show": 1, "remaining_sessions": 4, "status": "active"},
            id="valid-mixed-active",
        ),
        pytest.param(
            "clean-finish",
            ["attended", "cancelled", "attended"],
            2,
            False,
            {"used_sessions": 2, "remaining_sessions": 0, "status": "completed_successfully"},
            id="valid-clean-finish",
        ),
        pytest.param(
            "absence-finish",
            ["cancelled", "no_show"],
            1,
            False,
            {"used_sessions": 1, "remaining_sessions": 0, "status": "completed_with_absences"},
            id="valid-absence-finish",
        ),
    ],
)
def test_ai_method_valid_equivalence_groups_are_checked_by_partial_snapshots(
    label,
    history,
    package_sessions,
    member,
    expected,
) -> None:
    result = trainer(price=50.0).evaluate_client_package(history, package_sessions, member)

    assert {key: result[key] for key in expected} == expected


@pytest.mark.parametrize(
    ("operation", "message"),
    [
        pytest.param(
            lambda: trainer().evaluate_client_package("attended,no_show", 5, False),
            "invalid package data",
            id="history-string",
        ),
        pytest.param(
            lambda: trainer().evaluate_client_package([], 2.0, False),
            "invalid package data",
            id="package-float",
        ),
        pytest.param(
            lambda: trainer().evaluate_client_package([], 2, "yes"),
            "invalid package data",
            id="membership-string",
        ),
        pytest.param(
            lambda: trainer().evaluate_client_package(["attended", None], 5, False),
            "invalid session status",
            id="status-none",
        ),
        pytest.param(
            lambda: trainer().evaluate_client_package(["attended"] * 4, 3, False),
            "used sessions cannot exceed package sessions",
            id="history-consumes-too-much",
        ),
    ],
)
def test_ai_method_invalid_equivalence_groups_stop_at_the_expected_validation(
    operation,
    message,
) -> None:
    expect_value_error(operation, message)
