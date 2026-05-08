class FitnessClassBooking:
    """
    Clasa folosita pentru testarea unitara a unei singure functionalitati:
    evaluarea pachetului de sedinte al unui client.
    """

    VALID_CLASSES = {"dance", "pilates", "yoga", "zumba"}
    VALID_SESSION_STATUSES = {"attended", "no_show", "cancelled"}
    MAX_PACKAGE_SESSIONS = 20
    MEMBERSHIP_DISCOUNT = 0.20

    def __init__(
        self,
        class_name: str,
        instructor: str,
        price_per_session: float,
    ) -> None:
        if not isinstance(class_name, str) or class_name not in self.VALID_CLASSES:
            raise ValueError("class_name must be dance, pilates, yoga or zumba")
        if not isinstance(instructor, str) or not instructor.strip():
            raise ValueError("instructor must be a non-empty string")
        if (
            isinstance(price_per_session, bool)
            or not isinstance(price_per_session, (int, float))
            or price_per_session <= 0
        ):
            raise ValueError("price_per_session must be greater than 0")

        self.class_name = class_name
        self.instructor = instructor.strip()
        self.price_per_session = float(price_per_session)

    def evaluate_client_package(
        self,
        session_history: list[str],
        package_sessions: int,
        has_membership: bool,
    ) -> dict:
        """
        Evalueaza starea unui pachet de sedinte pentru un client.

        Statusuri acceptate in istoric:
        - attended: clientul a participat; sedinta se consuma
        - no_show: clientul nu a venit si nu a anuntat; sedinta se consuma
        - cancelled: clientul a anulat la timp; sedinta nu se consuma
        """
        if (
            not isinstance(session_history, list)
            or isinstance(package_sessions, bool)
            or not isinstance(package_sessions, int)
            or package_sessions < 1
            or package_sessions > self.MAX_PACKAGE_SESSIONS
            or not isinstance(has_membership, bool)
        ):
            raise ValueError("invalid package data")

        attended = 0
        no_show = 0
        cancelled = 0

        for session_status in session_history:
            if (
                not isinstance(session_status, str)
                or session_status not in self.VALID_SESSION_STATUSES
            ):
                raise ValueError("invalid session status")

            if session_status == "attended":
                attended += 1
            else:
                if session_status == "no_show":
                    no_show += 1
                if session_status == "cancelled":
                    cancelled += 1

        used_sessions = attended + no_show

        if used_sessions > package_sessions:
            raise ValueError("used sessions cannot exceed package sessions")

        remaining_sessions = package_sessions - used_sessions
        total_cost = package_sessions * self.price_per_session

        if has_membership:
            total_cost *= 1 - self.MEMBERSHIP_DISCOUNT

        if remaining_sessions == 0 and no_show == 0:
            status = "completed_clean"
        else:
            if remaining_sessions == 0:
                status = "completed"
            else:
                status = "active"

        return {
            "attended": attended,
            "no_show": no_show,
            "cancelled": cancelled,
            "used_sessions": used_sessions,
            "remaining_sessions": remaining_sessions,
            "total_cost": round(total_cost, 2),
            "status": status,
        }
