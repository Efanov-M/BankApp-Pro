from bank.user import User

from .transaction import Transaction, TransactionLog


class BankAccount:

    def __init__(self, user, balance):
        if not isinstance(user, User):
            raise ValueError("Ошибка: получатель должен быть объектом BankAccount")
        self.owner = user
        self.__balance = balance
        self._log = TransactionLog()  # для хранения операций текущего счёта.

    def get_balance(self):
        return self.__balance

    def set_balance(self, new_balance):
        if new_balance >= 0:
            self.__balance = new_balance
        else:
            print("Баланс не может быть отрицательным.")

    def deposit(self, amount):
        if amount >= 0:
            self.__balance = self.__balance + amount
            transaction = Transaction(
                type="deposit", amount=amount, sender=None, receiver=None, note=""
            )
            self._log.add(transaction)
            return self.__balance
        else:
            print("Сумма должна быть положительной.")

    def withdraw(self, amount):
        if amount < 0:
            print("Сумма должна быть положительной.")
            return
        if amount >= 0 and self.__balance >= amount:
            self.__balance = self.__balance - amount
            transaction = Transaction(
                type="withdraw",
                amount=amount,
                sender=self.owner,
                receiver=None,
                note="",
            )
            self._log.add(transaction)
            return self.__balance
        else:
            print("Недостаточно средств")

    def transfer(self, amount, other_account):
        if not isinstance(other_account, BankAccount):
            print("Ошибка: получатель должен быть объектом BankAccount")
            return
        if amount <= 0:
            print("Сумма перевода должна быть положительной.")
            return
        if self.__balance >= amount:
            self.__balance -= amount
            other_account.deposit(amount)
            transaction = Transaction(
                type="transfer",
                amount=amount,
                sender=self.owner,
                receiver=other_account.owner,
                note="",
            )
            self._log.add(transaction)
            # Лог у получателя
            incoming = Transaction(
                type="deposit",
                amount=amount,
                sender=self.owner,
                receiver=other_account.owner,
                note="Входящий перевод",
            )
            other_account._log.add(incoming)
            print(f"Переведено {amount} от {self.owner}к{other_account.owner}")
        else:
            print("Недостаточно средств для перевода.")

    def get_transaction_log(self):
        if not self._log._transactions:
            print("Нет операций по счёту.")
        else:
            for transaction in self._log._transactions:
                print(transaction)

    def filter_transactions_by_type(self, t_type):
        found = False
        for t in self._log._transactions:
            if t.type == t_type:
                print(t)
                found = True
        if not found:
            print(f"Нет операций типа: {t_type}")

    def filter_transactions_by_date(self, date_str):
        filtered = [
            t
            for t in self._log._transactions
            if t.timestamp.strftime("%d.%m.%Y") == date_str
        ]
        if not filtered:
            print(f"Нет операций за {date_str}")
        else:
            for t in filtered:
                print(t)

    def get_balance_with_history(self):
        print("===== Выписка по счёту =====")
        print(f"Владелец: {self.owner}")
        print(f"Текущий баланс: {self.get_balance():.2f} руб.")
        print()
        print("История операций:")
        if not self._log._transactions:
            print("Нет операций по счёту.")
        else:
            for t in self._log._transactions:
                print(t)

    def __str__(self):
        return f"Счёт владельца: {self.owner}— баланс: {self.__balance}"
