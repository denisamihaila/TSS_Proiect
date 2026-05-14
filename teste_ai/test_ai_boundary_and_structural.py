import pytest

from fitness_class_booking import FitnessClassBooking


def booking(price: float = 50.0) -> FitnessClassBooking:
    return FitnessClassBooking("dance", "Boundary AI", price)


@pytest.mark.parametrize(
    ("package_sessions", "history", "expected"),
    [
        pytest.param(
            1,
            ["cancelled"],
            {"used_sessions": 0, "remaining_sessions": 1, "status": "active"},
            id="lower-limit-not-consumed",
        ),
        pytest.param(
            1,
            ["attended"],
            {"used_sessions": 1, "remaining_sessions": 0, "status": "completed_successfully"},
            id="lower-limit-consumed-exactly",
        ),
        pytest.param(
            2,
            ["attended"],
            {"used_sessions": 1, "remaining_sessions": 1, "status": "active"},
            id="just-above-lower-limit",
        ),
        pytest.param(
            19,
            ["attended"] * 18,
            {"used_sessions": 18, "remaining_sessions": 1, "total_cost": 950.0},
            id="just-below-upper-limit",
        ),
        pytest.param(
            20,
            ["no_show"] + ["attended"] * 18,
            {
                "used_sessions": 19,
                "remaining_sessions": 1,
                "total_cost": 1000.0,
                "status": "active",
            },
            id="upper-limit-with-one-remaining",
        ),
    ],
)
def test_ai_boundary_package_size_edges_return_expected_state(
    package_sessions,
    history,
    expected,
) -> None:
    result = booking().evaluate_client_package(history, package_sessions, False)

    assert {key: result[key] for key in expected} == expected


def test_ai_boundary_upper_package_limit_can_finish_cleanly_with_membership_discount() -> None:
    result = booking().evaluate_client_package(["attended"] * 20, 20, True)

    expected = {
        "attended": 20,
        "used_sessions": 20,
        "remaining_sessions": 0,
        "total_cost": 800.0,
        "status": "completed_successfully",
    }
    assert {key: result[key] for key in expected} == expected


@pytest.mark.parametrize(
    "package_sessions",
    [
        pytest.param(-1, id="negative"),
        pytest.param(0, id="zero"),
        pytest.param(21, id="one-over-max"),
        pytest.param(100, id="far-over-max"),
        pytest.param(False, id="bool-false"),
    ],
)
def test_ai_boundary_invalid_package_sizes_share_the_same_guard(package_sessions) -> None:
    with pytest.raises(ValueError, match="^invalid package data$"):
        booking().evaluate_client_package([], package_sessions, False)


@pytest.mark.parametrize(
    ("price", "is_valid"),
    [
        pytest.param(0.001, True, id="small-positive"),
        pytest.param(0, False, id="zero"),
        pytest.param(True, False, id="bool-true"),
    ],
)
def test_ai_boundary_price_acceptance_is_based_on_positive_real_numbers(
    price,
    is_valid,
) -> None:
    if is_valid:
        assert FitnessClassBooking("dance", "Boundary AI", price).price_per_session == float(price)
    else:
        with pytest.raises(ValueError, match="^price_per_session must be greater than 0$"):
            FitnessClassBooking("dance", "Boundary AI", price)


@pytest.mark.parametrize(
    ("history", "package_sessions", "expected_status"),
    [
        pytest.param(["attended", "attended"], 2, "completed_successfully", id="tt-status-decision"),
        pytest.param(["attended", "no_show"], 2, "completed_with_absences", id="tf-status-decision"),
        pytest.param(["attended", "cancelled"], 3, "active", id="fx-status-decision"),
        pytest.param(["no_show"], 1, "completed_with_absences", id="absence-only-finish"),
        pytest.param(["cancelled"], 1, "active", id="cancelled-does-not-finish"),
    ],
)
def test_ai_structural_status_decision_outcomes_are_observable(
    history,
    package_sessions,
    expected_status,
) -> None:
    assert booking().evaluate_client_package(history, package_sessions, False)["status"] == expected_status


@pytest.mark.parametrize(
    ("price", "package_sessions", "member", "expected_total"),
    [
        pytest.param(12.345, 3, True, 29.63, id="discount-rounds-up"),
        pytest.param(19.995, 3, True, 47.99, id="discount-rounds-to-two-decimals"),
        pytest.param(19.995, 3, False, 59.98, id="no-discount-same-rounding-rule"),
    ],
)
def test_ai_structural_cost_branch_and_rounding_are_visible(
    price,
    package_sessions,
    member,
    expected_total,
) -> None:
    result = booking(price).evaluate_client_package(["cancelled"], package_sessions, member)

    assert result["total_cost"] == expected_total
