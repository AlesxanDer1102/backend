from abc import ABC, abstractmethod
from datetime import date, timedelta

from domain.loan import Loan
from domain.enums.estado_prestamos import EstadoPrestamo


# patron factory method: clase Creator abstracta que declara el factory
# method `create_loan()`. Cada subclase concreta decide la politica de
# prestamo (plazo de devolucion) con la que se construye el objeto Loan.
class LoanFactory(ABC):
    """
    Creator abstracto del patron Factory Method.

    Declara `create_loan()`, el factory method que devuelve un objeto de
    dominio `Loan` ya construido y listo para persistir. Las subclases
    concretas (ConcreteCreator) deciden la politica de prestamo aplicada
    sin que el cliente conozca el detalle.
    """

    @abstractmethod
    def create_loan(self, user_id: int, copy_code: str) -> Loan:
        """Factory method: construye un Loan segun la politica de la subclase."""
        ...

    def _build_active_loan(
        self,
        user_id: int,
        copy_code: str,
        loan_period_days: int,
    ) -> Loan:
        """
        Helper compartido por las subclases: arma un prestamo ACTIVO cuya
        fecha de vencimiento depende del plazo propio de cada politica.
        Centraliza la construccion correcta del Loan (estado, fechas, id).
        """
        approval_date = date.today()
        return Loan(
            id=None,
            user_id=user_id,
            copy_code=copy_code,
            aproval_date=approval_date,
            due_date=approval_date + timedelta(days=loan_period_days),
            retrival_date=None,
            status=EstadoPrestamo.ACTIVO,
        )


class StandardLoanFactory(LoanFactory):
    """ConcreteCreator: prestamo estandar para libros de circulacion general."""

    LOAN_PERIOD_DAYS = 14

    def create_loan(self, user_id: int, copy_code: str) -> Loan:
        return self._build_active_loan(user_id, copy_code, self.LOAN_PERIOD_DAYS)


class ShortTermLoanFactory(LoanFactory):
    """ConcreteCreator: prestamo express para material de alta demanda."""

    LOAN_PERIOD_DAYS = 3

    def create_loan(self, user_id: int, copy_code: str) -> Loan:
        return self._build_active_loan(user_id, copy_code, self.LOAN_PERIOD_DAYS)


class ExtendedLoanFactory(LoanFactory):
    """ConcreteCreator: prestamo extendido para docentes o investigadores."""

    LOAN_PERIOD_DAYS = 30

    def create_loan(self, user_id: int, copy_code: str) -> Loan:
        return self._build_active_loan(user_id, copy_code, self.LOAN_PERIOD_DAYS)
