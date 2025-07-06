from .cliente_decorator import ClienteDecorator

class CashbackDecorator(ClienteDecorator):
    def __init__(self, cliente, cashback):
        super().__init__(cliente)
        self.cashback = cashback
    def get_cashback(self):
        return self.cashback
