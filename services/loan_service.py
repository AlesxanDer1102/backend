from domain.loan import Loan
from repositories.loan_repository import LoanRepository
from services.loan_factory import LoanFactory


class LoanService:
    """
    Servicio de aplicacion para la gestion de prestamos.

    Es el cliente del patron Factory Method: trabaja contra el tipo
    abstracto `LoanFactory` y no conoce la politica concreta con la que
    se construye cada `Loan` (estandar, express, extendido, etc.).
    """

    def __init__(self, loan_repo: LoanRepository) -> None:
        self.repo = loan_repo

    async def register_loan(
        self,
        user_id: int,
        copy_code: str,
        factory: LoanFactory,
    ) -> Loan:
        # patron factory method: se delega la construccion del Loan a la
        # factory recibida; el servicio ignora la politica concreta aplicada.
        loan = factory.create_loan(user_id, copy_code)
        return self.repo.create(loan)
