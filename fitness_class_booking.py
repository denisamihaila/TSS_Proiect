class FitnessClassBooking:
    """
    Evaluarea pachetului de sedinte al unui client.
    """

    # Valorile permise pentru tipul clasei de fitness si pentru statusurile din istoricul sedintelor
    VALID_CLASSES = {"dance", "pilates", "yoga", "zumba"}
    VALID_SESSION_STATUSES = {"attended", "no_show", "cancelled"}

    # Limita superioara de sesiuni a unui pachet si reducerea aplicata clientilor care au membership
    MAX_PACKAGE_SESSIONS = 20
    MEMBERSHIP_DISCOUNT = 0.20

    def __init__(
        self,
        class_name: str,
        instructor: str,
        price_per_session: float,
    ) -> None:
        # class_name trebuie sa fie text si sa faca parte din lista de clase acceptate
        if not isinstance(class_name, str) or class_name not in self.VALID_CLASSES:
            raise ValueError("class_name must be dance, pilates, yoga or zumba")

        # instructor trebuie sa fie un sir nevid
        # strip() elimina spatiile de la inceput si de la final, astfel incat "   " devine invalid
        if not isinstance(instructor, str) or not instructor.strip():
            raise ValueError("instructor must be a non-empty string")

        # price_per_session trebuie sa fie numar pozitiv
        # bool este verificat separat deoarece in Python bool este subclasa de int
        if (
            isinstance(price_per_session, bool)
            or not isinstance(price_per_session, (int, float))
            or price_per_session <= 0
        ):
            raise ValueError("price_per_session must be greater than 0")

        # dupa validare, valorile sunt salvate pe obiect
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
        Evalueaza starea unui pachet de sedinte pentru un client

        Statusuri acceptate in istoric:
        - attended: clientul a participat; sedinta se consuma
        - no_show: clientul nu a venit si nu a anuntat; sedinta se consuma
        - cancelled: clientul a anulat la timp; sedinta nu se consuma
        """
        # validarea generala a parametrilor metodei: numarul de sesiuni ale pachetului trebuie sa fie
        # intre 1 si MAX_PACKAGE_SESSIONS, iar has_membership trebuie sa fie strict boolean
        if (
            not isinstance(session_history, list)
            or isinstance(package_sessions, bool)
            or not isinstance(package_sessions, int)
            or package_sessions < 1
            or package_sessions > self.MAX_PACKAGE_SESSIONS
            or not isinstance(has_membership, bool)
        ):
            raise ValueError("invalid package data")

        # contoarele pornesc de la 0 si vor fi actualizate in functie de
        # fiecare status gasit in istoricul sedintelor
        attended = 0
        no_show = 0
        cancelled = 0

        for session_status in session_history:
            # fiecare element din istoric trebuie sa fie un status cunoscut.
            # orice valoare diferita opreste evaluarea pachetului
            if (
                not isinstance(session_status, str)
                or session_status not in self.VALID_SESSION_STATUSES
            ):
                raise ValueError("invalid session status")

            # o sedinta attended se numara ca participare si consuma o sedinta din pachet
            if session_status == "attended":
                attended += 1
            else:
                # pentru ramura else raman statusurile no_show si cancelled.
                # no_show consuma sedinta, cancelled doar se numara separat
                if session_status == "no_show":
                    no_show += 1
                if session_status == "cancelled":
                    cancelled += 1

        # sedintele consumate sunt cele attended plus cele no_show. anularile la timp nu consuma sedinte
        used_sessions = attended + no_show

        # nu este posibil ca istoricul sa consume mai multe sedinte decat numarul celor din pachet
        if used_sessions > package_sessions:
            raise ValueError("used sessions cannot exceed package sessions")

        # calculam sedintele ramase si costul de baza al intregului pachet
        remaining_sessions = package_sessions - used_sessions
        total_cost = package_sessions * self.price_per_session

        # clientii cu membership primesc reducerea configurata la nivelul clasei.
        if has_membership:
            total_cost *= 1 - self.MEMBERSHIP_DISCOUNT

        # statusul final descrie daca pachetul mai este activ sau a fost
        # finalizat cu succes ori cu absente.
        if remaining_sessions == 0 and no_show == 0:
            status = "completed_successfully"
        else:
            if remaining_sessions == 0:
                status = "completed_with_absences"
            else:
                status = "active"

        # rezultatul este intors ca dictionar
        return {
            "attended": attended,
            "no_show": no_show,
            "cancelled": cancelled,
            "used_sessions": used_sessions,
            "remaining_sessions": remaining_sessions,
            "total_cost": round(total_cost, 2),
            "status": status,
        }
