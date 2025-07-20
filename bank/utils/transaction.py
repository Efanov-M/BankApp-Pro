from datetime import datetime


class Transaction:  # представляет одну операцию (deposit, withdraw, transfer).

    def __init__(self, type, amount, sender=None, receiver=None, note=""):
        self.type = type
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.note = note
        self.timestamp = datetime.now()

    def __str__(self):
        date = self.timestamp.strftime("%d.%m.%Y")
        note_part = f" ({self.note})" if self.note else ""

        if self.type == "deposit":
            return f"{date} deposit: +{self.amount:.2f}{note_part}"
        elif self.type == "transfer":
            return f"{date} transfer: -{self.amount:.2f} from {self.sender} to {self.receiver}{note_part}"
        elif self.type == "withdraw":
            return f"{date} withdraw: -{self.amount:.2f}{note_part}"
        else:
            return f"{date} Неизвестная операция: тип = {self.type}"

    def to_dict(self):

        # Преобразует объект Transaction в словарь для сохранения в JSON.

        return {
            "type": self.type,  # Тип транзакции: deposit, withdraw, transfer
            "amount": self.amount,  # Сумма
            "sender": (
                self.sender.user_id if self.sender else None
            ),  # ID отправителя, если есть
            "receiver": (
                self.receiver.user_id if self.receiver else None
            ),  # ID получателя, если есть
            "note": self.note,  # Комментарий
            "timestamp": self.timestamp.isoformat(),  # Дата/время в строковом формате ISO 8601
        }

    @classmethod
    def from_dict(cls, data):
        from datetime import datetime

        from bank.user import User  # Нужно для создания временных объектов

        # Временные "заглушки" пользователей — заменяются позже
        sender = (
            User(username="sender", email="none@example.com", user_id=data["sender"])
            if data["sender"]
            else None
        )
        receiver = (
            User(
                username="receiver", email="none@example.com", user_id=data["receiver"]
            )
            if data["receiver"]
            else None
        )

        # Восстановление объекта Transaction
        obj = cls(
            type=data["type"],
            amount=data["amount"],
            sender=sender,
            receiver=receiver,
            note=data["note"],
        )

        # Восстанавливаем точное время
        obj.timestamp = datetime.fromisoformat(data["timestamp"])

        return obj


class TransactionLog:  # журнал всех операций, умеет добавлять, фильтровать и выводить список.

    def __init__(self):

        self._transactions = []  # список куда скидываем все обьекты по операциям

    def add(self, transaction):
        if isinstance(transaction, Transaction):
            self._transactions.append(transaction)
        else:
            print("Ошибка: можно добавлять только объекты Transaction")

    def show_all(self, t_type):
        return [t for t in self._transactions if t.type == t_type]

    def filter_by_date(self, date_str):
        filtered = [
            t
            for t in self._transactions
            if t.timestamp.strftime("%d.%m.%Y") == date_str
        ]
        if not filtered:
            print(f"Нет операций за {date_str}")
        return filtered

    def to_dict(self):

        return [transaction.to_dict() for transaction in self._transactions]
