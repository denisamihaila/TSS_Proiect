class FitnessClassBooking:
    """
    AI-only copy of the project class used for comparison tests.

    This copy keeps the same behavior as the main module, but it also treats
    bool as invalid for price_per_session so the AI suite can document that
    edge case in isolation.
    """

    VALID_CLASSES = {"dance", "pilates", "yoga", "zumba"}
    MAX_WAITLIST_SIZE = 5

    def __init__(
        self,
        class_name: str,
        instructor: str,
        max_spots: int,
        price_per_session: float,
    ) -> None:
        if class_name not in self.VALID_CLASSES:
            raise ValueError(
                f"class_name must be one of {sorted(self.VALID_CLASSES)}, got '{class_name}'"
            )
        if not isinstance(instructor, str) or not instructor or not instructor.strip():
            raise ValueError("instructor must be a non-empty string")
        if isinstance(max_spots, bool) or not isinstance(max_spots, int) or max_spots < 1 or max_spots > 30:
            raise ValueError("max_spots must be an integer between 1 and 30 inclusive")
        if isinstance(price_per_session, bool) or not isinstance(price_per_session, (int, float)) or price_per_session <= 0:
            raise ValueError("price_per_session must be greater than 0")

        self.class_name: str = class_name
        self.instructor: str = instructor.strip()
        self.max_spots: int = max_spots
        self.price_per_session: float = float(price_per_session)
        self.booked_spots: int = 0
        self.waitlist: list = []
        self._confirmed: list = []

    # ------------------------------------------------------------------
    def book_spot(self, client_name: str) -> str:
        if not isinstance(client_name, str) or not client_name or not client_name.strip():
            raise ValueError("client_name must be a non-empty string")

        client = client_name.strip()

        if self.booked_spots < self.max_spots:
            self._confirmed.append(client)
            self.booked_spots += 1
            return "confirmed"
        elif len(self.waitlist) < self.MAX_WAITLIST_SIZE:
            self.waitlist.append(client)
            return "waitlist"
        else:
            return "rejected"

    # ------------------------------------------------------------------
    def cancel_booking(self, client_name: str) -> bool:
        name = client_name.strip() if client_name else ""

        if name in self._confirmed:
            self._confirmed.remove(name)
            self.booked_spots -= 1
            if self.waitlist:
                promoted = self.waitlist.pop(0)
                self._confirmed.append(promoted)
                self.booked_spots += 1
            return True
        elif name in self.waitlist:
            self.waitlist.remove(name)
            return True
        else:
            return False

    # ------------------------------------------------------------------
    def calculate_cost(self, sessions: int, has_membership: bool) -> float:
        if not isinstance(sessions, int) or isinstance(sessions, bool) or sessions < 1 or sessions > 20:
            raise ValueError(
                f"sessions must be between 1 and 20 inclusive, got {sessions}"
            )

        cost = sessions * self.price_per_session

        discount = 0.0
        if has_membership:
            discount += 0.20
        if sessions >= 10:
            discount += 0.10

        return round(cost * (1 - discount), 2)
