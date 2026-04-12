"""
fitness_class_booking.py – Implementarea clasei FitnessClassBooking.

Proiect universitar TSS – T1 Testare unitară Python.
"""


class FitnessClassBooking:
    """
    Manages bookings for a fitness class session.

    Supports confirmed spots, a waitlist of up to 5 people, and cancellations
    with automatic promotion from the waitlist.

    Attributes:
        class_name          One of: "dance", "pilates", "yoga", "zumba"
        instructor          Non-empty string
        max_spots           Integer 1–30
        price_per_session   Float > 0
        booked_spots        Current confirmed bookings (starts at 0)
        waitlist            List of waitlisted client names (max 5)
        _confirmed          Internal list of confirmed client names
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
        """
        Initialize a FitnessClassBooking session.

        :param class_name:          Type of class. Must be one of VALID_CLASSES.
        :param instructor:          Instructor name. Non-empty string.
        :param max_spots:           Capacity. Integer between 1 and 30 inclusive.
        :param price_per_session:   Price per session. Must be > 0.
        :raises ValueError: If any parameter fails validation.
        """
        if class_name not in self.VALID_CLASSES:
            raise ValueError(
                f"class_name must be one of {sorted(self.VALID_CLASSES)}, got '{class_name}'"
            )
        if not instructor or not instructor.strip():
            raise ValueError("instructor must be a non-empty string")
        if not isinstance(max_spots, int) or isinstance(max_spots, bool) \
                or max_spots < 1 or max_spots > 30:
            raise ValueError("max_spots must be an integer between 1 and 30 inclusive")
        if price_per_session <= 0:
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
        """
        Attempt to book a spot for a client.

        :param client_name: Name of the client. Must be a non-empty string.
        :return:
            "confirmed" – spot booked successfully.
            "waitlist"  – class full but waitlist has room (< 5 people).
            "rejected"  – class full and waitlist full (5 people).
        :raises ValueError: If client_name is empty or whitespace-only.
        """
        if not client_name or not client_name.strip():
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
        """
        Cancel a booking for a client.

        If the client has a confirmed spot, it is freed and the first person
        on the waitlist (if any) is automatically promoted to confirmed.

        :param client_name: Name of the client whose booking to cancel.
        :return: True if a booking was found and cancelled, False otherwise.
        """
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
        """
        Calculate the total cost for a number of sessions.

        Discount rules (applied cumulatively in order):
            1. Membership discount:  20% off base cost  (if has_membership).
            2. Volume discount:      10% off             (if sessions >= 10).

        :param sessions:        Number of sessions. Must be in [1, 20].
        :param has_membership:  Whether the client has an active membership.
        :return: Total cost rounded to 2 decimal places.
        :raises ValueError: If sessions < 1 or sessions > 20.
        """
        if sessions < 1 or sessions > 20:
            raise ValueError(
                f"sessions must be between 1 and 20 inclusive, got {sessions}"
            )

        cost = sessions * self.price_per_session

        if has_membership:
            cost *= 0.80  # 20% membership discount

        if sessions >= 10:
            cost *= 0.90  # additional 10% volume discount

        return round(cost, 2)

    # ------------------------------------------------------------------
    def get_availability(self) -> dict:
        """
        Return the current availability status of the class.

        :return: Dictionary with keys:
                    "free"     – remaining bookable spots
                    "booked"   – current confirmed bookings
                    "waitlist" – number of people on the waitlist
        """
        return {
            "free": self.max_spots - self.booked_spots,
            "booked": self.booked_spots,
            "waitlist": len(self.waitlist),
        }
