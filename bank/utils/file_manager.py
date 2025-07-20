import json  # Подключаем модуль для работы с JSON (сериализация словарей в строку и обратно)
import os  # Подключаем модуль для работы с файловой системой (создание папок, проверка путей)


def save_users(users: dict) -> None:
    from bank.user import (
        User,  # Локальный импорт класса User, чтобы избежать циклических зависимостей
    )

    data = {}
    # Создаём временный словарь, куда запишем всех пользователей в формате "user_id": {данные}

    for user_id, user_obj in users.items():  # Проходим по всем парам в словаре users
        if isinstance(user_obj, User):
            # Проверяем, что значение — это действительно объект класса User
            data[user_id] = user_obj.to_dict()
            # Преобразуем объект User в словарь и сохраняем в data
    # Создаём папку bank/data, если её ещё нет (без ошибки, если уже есть)
    os.makedirs("bank/data", exist_ok=True)
    # Открываем файл для записи (перезапишется при необходимости)
    with open("bank/data/users.json", "w") as f:
        json.dump(data, f, indent=4)
        # Записываем словарь data в JSON-файл с отступами для читаемости


def load_users() -> dict:
    from bank.user import (
        User,  # Локальный импорт класса User, чтобы избежать циклических импортов
    )

    # Создаём пустой словарь, куда будем загружать восстановленных пользователей
    users = {}

    if os.path.isfile("bank/data/users.json"):
        with open("bank/data/users.json", "r", encoding="utf-8") as f:
            data_file = json.load(f)
            # Загружаем данные из JSON-файла в виде словаря

            for user_id, user_dict in data_file.items():
                # Проходим по каждому пользователю (ключ + словарь данных)
                users[user_id] = User.from_dict(user_dict)
                # Восстанавливаем объект User из словаря и сохраняем в итоговый словарь

    return users  # Возвращаем словарь пользователей (может быть пустым, если файл не найден)


def save_accounts(accounts: dict) -> None:
    from bank.utils.account import BankAccount

    data = {}  # Новый словарь для сериализации

    for account_id, account_obj in accounts.items():
        if isinstance(account_obj, BankAccount):
            data[account_id] = account_obj.to_dict()  # Преобразуем объект в словарь

    os.makedirs("bank/data", exist_ok=True)  # Создаём папку, если нет
    with open("bank/data/accounts.json", "w") as f:
        json.dump(data, f, indent=4)  # Сохраняем как JSON


def load_accounts() -> dict:
    from bank.utils.account import BankAccount

    accounts = {}

    if os.path.isfile("bank/data/accounts.json"):
        with open("bank/data/accounts.json", "r", encoding="utf-8") as f:
            data_file = json.load(f)
            for account_id, account_dict in data_file.items():
                accounts[account_id] = BankAccount.from_dict(account_dict)

    return accounts


def save_logs(logs: dict):
    from bank.utils.transaction import Transaction, TransactionLog

    logi = {}

    for account_id, logs_obj in logs.items():
        if isinstance(logs_obj, TransactionLog):
            logi[account_id] = logs_obj.to_dict()  # Список словарей транзакций

    os.makedirs("bank/data", exist_ok=True)
    with open("bank/data/logs.json", "w", encoding="utf-8") as f:
        json.dump(logi, f, indent=4)


def load_logs() -> dict:
    import json
    import os

    from bank.utils.transaction import (  # Локальный импорт классов
        Transaction,
        TransactionLog,
    )

    logs = {}  # Словарь, куда будем складывать восстановленные журналы транзакций

    if os.path.isfile("bank/data/logs.json"):  # Проверяем, существует ли файл
        with open("bank/data/logs.json", "r", encoding="utf-8") as f:
            data = json.load(f)  # Загружаем содержимое JSON-файла как словарь

            for account_id, tx_list in data.items():  # Проходим по каждому счёту
                log = TransactionLog()  # Новый журнал для этого счёта

                for tx_data in tx_list:  # Проходим по списку транзакций
                    transaction = Transaction.from_dict(
                        tx_data
                    )  # Восстанавливаем объект Transaction
                    log.add(transaction)  # Добавляем в журнал

                logs[account_id] = log  # Сохраняем журнал в итоговый словарь

    return logs  # Возвращаем словарь с журналами транзакций
