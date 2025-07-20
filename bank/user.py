from bank.utils.account import BankAccount


class User:

    # Класс для представления пользователя банка.

    # Атрибуты:
    # username — имя пользователя
    # email — адрес электронной почты
    # user_id — уникальный ID
    # accounts — список банковских счетов

    def __init__(
        self,
        username,
        email,
        user_id,
    ):
        self.username = username
        if not self.is_valid_email(email):
            raise ValueError("Некорректный email")
        self.email = email
        self.user_id = user_id
        self.accounts = []

    def is_valid_email(self, email):
        return "@" in email and "." in email.split("@")[-1]

    def update_email(self, new_email):
        if not self.is_valid_email(new_email):
            raise ValueError("Некорректный email")
        self.email = new_email

    def add_account(self, account):
        if not isinstance(account, BankAccount):
            raise ValueError("Ошибка: получатель должен быть объектом BankAccount")

        self.accounts.append(account)

    def list_accounts(self):
        if not self.accounts:
            print("Нет открытых счетов")
        else:
            print(f"Счета пользователя {self.username}:")
            for ac in self.accounts:
                print(f"- {ac}")

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"], email=data["email"], user_id=data["user_id"]
        )

    def __str__(self):
        return (
            f"У пользователя {self.username} с id: {self.user_id} email: {self.email}"
        )
