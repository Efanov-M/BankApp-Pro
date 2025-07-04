from datetime import datetime


class Transaction: #представляет одну операцию (deposit, withdraw, transfer).
    
    def __init__(self, type, amount, sender=None, receiver=None, note=""):
        self.type = type
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.note = note
        self.timestamp = datetime.now()
        
    def __str__(self):
        date = self.timestamp.strftime('%d.%m.%Y')
        note_part = f" ({self.note})" if self.note else ""

        if self.type == "deposit":
            return f"{date} deposit: +{self.amount:.2f}{note_part}"
        elif self.type == "transfer":
            return f"{date} transfer: -{self.amount:.2f} from {self.sender} to {self.receiver}{note_part}"
        elif self.type == "withdraw":
            return f"{date} withdraw: -{self.amount:.2f}{note_part}"
        else:
            return f"{date} Неизвестная операция: тип = {self.type}"
    
    
class TransactionLog: #журнал всех операций, умеет добавлять, фильтровать и выводить список.
    
    def __init__(self):
        
        self._transactions = [] #список куда скидываем все обьекты по операциям
        
    def add(self, transaction):
        if isinstance(transaction, Transaction):
            self._transactions.append(transaction)
        else:
            print("Ошибка: можно добавлять только объекты Transaction")
            
    def show_all(self, t_type):
        return [t for t in self._transactions if t.type == t_type]
        
    def filter_by_date(self, date_str):
        filtered = [t for t in self._transactions if t.timestamp.strftime('%d.%m.%Y') == date_str]
        if not filtered:
            print(f"Нет операций за {date_str}")
        return filtered
    

class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance
        self._log = TransactionLog() #для хранения операций текущего счёта.

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
            transaction = Transaction (type = 'deposit', amount=amount, sender=None, receiver=None, note="")
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
            transaction = Transaction (type = 'withdraw', amount=amount, sender=self.owner, receiver=None, note="")
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
            transaction = Transaction (type = 'transfer', amount=amount, sender=self.owner, receiver=other_account.owner, note="")
            self._log.add(transaction)
            # Лог у получателя
            incoming = Transaction(
            type='deposit',
            amount=amount,
            sender=self.owner,
            receiver=other_account.owner,
            note="Входящий перевод"
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
            
        

    def __str__(self):
        return f"Счёт владельца: {self.owner}— баланс: {self.__balance}"

    
