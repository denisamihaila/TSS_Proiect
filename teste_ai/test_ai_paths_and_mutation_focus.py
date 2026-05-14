import pytest

from fitness_class_booking import FitnessClassBooking


def booking(price: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("zumba", "Path AI", price)


def result_for(history, package_sessions=6, member=False, price=50.0) -> dict:
    return booking(price).evaluate_client_package(history, package_sessions, member)


def test_ai_path_order_of_valid_statuses_does_not_change_aggregate_counts() -> None:
    first = result_for(["attended", "cancelled", "no_show", "attended"], 5)
    second = result_for(["no_show", "attended", "attended", "cancelled"], 5)

    comparable_keys = ("attended", "no_show", "cancelled", "used_sessions", "remaining_sessions", "status")
    assert {key: first[key] for key in comparable_keys} == {
        key: second[key] for key in comparable_keys
    }


def test_ai_mutation_status_matching_uses_value_equality_for_dynamic_strings() -> None:
    history = [
        "".join(("att", "ended")),
        "_".join(("no", "show")),
        "".join(("cancel", "led")),
    ]

    result = result_for(history, package_sessions=3)

    assert history == ["attended", "no_show", "cancelled"]
    assert result["attended"] == 1
    assert result["no_show"] == 1
    assert result["cancelled"] == 1
    assert result["used_sessions"] == 2
    assert result["remaining_sessions"] == 1


def test_ai_path_inserted_cancellations_do_not_change_consumption_or_price() -> None:
    compact = result_for(["attended", "no_show"], 4, member=True, price=80.0)
    padded = result_for(
        ["cancelled", "attended", "cancelled", "no_show", "cancelled"],
        4,
        member=True,
        price=80.0,
    )

    assert padded["cancelled"] == compact["cancelled"] + 3
    assert padded["used_sessions"] == compact["used_sessions"]
    assert padded["remaining_sessions"] == compact["remaining_sessions"]
    assert padded["total_cost"] == compact["total_cost"]


def test_ai_path_package_data_validation_masks_session_status_validation() -> None:
    with pytest.raises(ValueError, match="^invalid package data$"):
        result_for(["not-a-real-status"], package_sessions=0)


def test_ai_path_session_status_validation_happens_before_consumption_overflow() -> None:
    with pytest.raises(ValueError, match="^invalid session status$"):
        result_for(["attended", "ghost", "attended"], package_sessions=1)


def test_ai_path_overflow_is_checked_after_all_valid_statuses_are_counted() -> None:
    with pytest.raises(ValueError, match="^used sessions cannot exceed package sessions$"):
        result_for(["cancelled", "attended", "no_show", "cancelled"], package_sessions=1)


def test_ai_mutation_total_cost_depends_on_package_size_not_on_used_sessions() -> None:
    barely_used = result_for(["cancelled"], package_sessions=8, price=45.0)
    mostly_used = result_for(["attended", "attended", "no_show"], package_sessions=8, price=45.0)

    assert barely_used["used_sessions"] != mostly_used["used_sessions"]
    assert barely_used["total_cost"] == mostly_used["total_cost"] == 360.0


def test_ai_mutation_discounted_total_is_exactly_the_configured_ratio() -> None:
    full_price = result_for([], package_sessions=5, member=False, price=70.0)
    member_price = result_for([], package_sessions=5, member=True, price=70.0)

    expected_discounted_total = round(
        full_price["total_cost"] * (1 - FitnessClassBooking.MEMBERSHIP_DISCOUNT),
        2,
    )
    assert member_price["total_cost"] == expected_discounted_total


@pytest.mark.parametrize(
    ("history", "package_sessions", "expected"),
    [
        pytest.param(
            ["attended"] * 20,
            20,
            {"attended": 20, "used_sessions": 20, "status": "completed_successfully"},
            id="twenty-attended-sessions",
        ),
        pytest.param(
            ["no_show"] * 20,
            20,
            {"no_show": 20, "used_sessions": 20, "status": "completed_with_absences"},
            id="twenty-no-show-sessions",
        ),
        pytest.param(
            ["cancelled"] * 20,
            20,
            {"cancelled": 20, "used_sessions": 0, "status": "active"},
            id="twenty-cancelled-sessions",
        ),
    ],
)
def test_ai_mutation_repeated_statuses_are_accumulated_not_collapsed(
    history,
    package_sessions,
    expected,
) -> None:
    result = result_for(history, package_sessions=package_sessions)

    assert {key: result[key] for key in expected} == expected


@pytest.mark.parametrize(
    ("operation", "message"),
    [
        pytest.param(
            lambda: FitnessClassBooking("zumba", "Path AI", False),
            "price_per_session must be greater than 0",
            id="constructor-bool-price",
        ),
        pytest.param(
            lambda: result_for([], package_sessions=True),
            "invalid package data",
            id="method-bool-package",
        ),
        pytest.param(
            lambda: result_for([], package_sessions=3, member=1),
            "invalid package data",
            id="method-int-membership",
        ),
    ],
)
def test_ai_mutation_bool_values_are_not_silently_treated_as_numbers(
    operation,
    message,
) -> None:
    with pytest.raises(ValueError, match=f"^{message}$"):
        operation()
