

class BankClient:
    """Represents a bank client"""
    def __init__(self, client_id, name, surname):
        self.id = client_id
        self.name = name
        self.surname = surname

    def __eq__(self, other)->bool:
        if isinstance(other, BankClient):
            return self.id == other.id
        elif isinstance(other, int):
            return self.id == other
        elif isinstance(other, str):
            return self.name+" "+self.surname == other

    def __lt__(self, other)->bool:
        if isinstance(other, BankClient):
            return self.id < other.id
        elif isinstance(other, int):
            return self.id < other
        elif isinstance(other, str):
            return self.name+" "+self.surname < other

    def __str__(self):
        return f"CLIENT {self.id}: {self.name} {self.surname}"
