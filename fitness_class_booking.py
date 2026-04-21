class FitnessClassBooking:
    """
    Gestionează rezervările pentru o ședință de fitness.

    Atribute:
        class_name          "dance", "pilates", "yoga" sau "zumba"
        instructor          Șir nevid
        max_spots           nr intreg 1–30
        price_per_session   float > 0
        booked_spots        locuri confirmate (>=0)
        waitlist            Listă de așteptare (max 5 persoane)
        _confirmed          Listă internă a clienților confirmați
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
        if not isinstance(price_per_session, (int, float)) or price_per_session <= 0:
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
        """Rezervă un loc: returnează 'confirmed', 'waitlist' sau 'rejected'.
        Ridică ValueError dacă client_name este gol sau non-string."""
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
        """Anulează rezervarea clientului; promovează automat primul client din waitlist.
        Returnează True dacă rezervarea a fost găsită, False altfel."""
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
        """Calculează costul total pentru un număr de ședințe (între 1 și 20).
        Reduceri aplicate aditiv față de prețul de bază:
        - −20% dacă has_membership este True
        - −10% dacă sessions >= 10 (reducere de volum)
        Ridică ValueError dacă sessions nu este întreg sau este în afara [1, 20]."""
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
