# bank/cli.py

import argparse

from bank.user import User
from bank.utils.account import BankAccount
from bank.utils.file_manager import save_accounts, save_logs, save_users
from bank.utils.transaction import Transaction, TransactionLog

USERS = {}
ACCOUNTS = {}
LOGS = {}


def main():
    parser = argparse.ArgumentParser(description="Bank CLI")
    subparsers = parser.add_subparsers(dest="command")

    # TODO: здесь будут команды
    # create-user
    create_user = subparsers.add_parser(
        "create-user", help="Создать нового пользователя."
    )
    group_create_user = create_user.add_argument_group("создание нового пользователя")
    group_create_user.add_argument(
        "-n", "--name", type=str, required=True, help="Имя пользователя"
    )
    group_create_user.add_argument("--email", required=True, type=str, help="Email")
    group_create_user.add_argument(
        "--id", required=True, type=int, help="Уникальный ID"
    )

    # create-account
    create_account = subparsers.add_parser(
        "create-account", help="Создать счёт для пользователя."
    )
    group_create_account = create_account.add_argument_group("создание счёта")
    group_create_account.add_argument(
        "--user-id", required=True, type=int, help="ID пользователя"
    )
    group_create_account.add_argument(
        "--balance", default=0, type=float, help="Начальный баланс"
    )

    # deposit
    deposit = subparsers.add_parser("deposit", help="Пополнить счёт.")
    group_deposit = deposit.add_argument_group("пополнение")
    group_deposit.add_argument(
        "--user-id", type=int, required=True, help="ID пользователя"
    )
    group_deposit.add_argument(
        "--amount", type=float, required=True, help="Сумма пополнения"
    )

    # withdraw
    withdraw_ = subparsers.add_parser("withdraw", help="Снять деньги со счёта.")
    group_withdraw = withdraw_.add_argument_group("снятие")
    group_withdraw.add_argument(
        "--user-id", type=int, required=True, help="ID пользователя"
    )
    group_withdraw.add_argument(
        "--amount", type=float, required=True, help="Сумма снятия"
    )

    # transfer
    transfer = subparsers.add_parser(
        "transfer", help="Перевести средства между счетами."
    )
    group_transfer = transfer.add_argument_group("перевод")
    group_transfer.add_argument(
        "--from_user_id", required=True, type=int, help="ID отправителя"
    )
    group_transfer.add_argument(
        "--to_user_id", required=True, type=int, help="ID получателя"
    )
    group_transfer.add_argument(
        "--amount", required=True, type=float, help="Сумма перевода"
    )

    # show-balance
    show_balance = subparsers.add_parser(
        "show-balance", help="Показать текущий баланс счёта."
    )
    group_balance = show_balance.add_argument_group("баланс")
    group_balance.add_argument(
        "--user-id", required=True, type=int, help="ID пользователя"
    )

    # show-log
    show_log = subparsers.add_parser(
        "show-log", help="Показать историю операций пользователя."
    )
    group_log = show_log.add_argument_group("журнал")
    group_log.add_argument("--user-id", required=True, type=int, help="ID пользователя")

    # fс
    filter_type = subparsers.add_parser(
        "filter-type", help="Фильтровать операции по типу."
    )
    group_ftype = filter_type.add_argument_group("фильтр по типу")
    group_ftype.add_argument(
        "--user-id", required=True, type=int, help="ID пользователя"
    )
    group_ftype.add_argument(
        "--type",
        choices=["deposit", "withdraw", "transfer"],
        required=True,
        type=str,
        help="Тип транзакции (deposit/withdraw/transfer)",
    )
    # filter-date
    filter_date = subparsers.add_parser(
        "filter-date", help="Фильтровать операции по дате."
    )
    group_fdate = filter_date.add_argument_group("фильтр по дате")
    group_fdate.add_argument(
        "--user-id", required=True, type=int, help="ID пользователя"
    )
    group_fdate.add_argument(
        "--date", required=True, type=str, help="Дата в формате ДД.ММ.ГГГГ"
    )

    # exit (в обработке команд, а не через argparse — exit просто прерывает цикл)

    args = parser.parse_args()

    # Проверяем, что активная команда — это 'create-user'
    if args.command == "create-user":
        user_id = args.id  # Сохраняем ID пользователя из аргументов
        username = args.name  # Имя пользователя
        email = args.email  # Email пользователя

        # Проверяем, существует ли уже пользователь с таким ID
        if user_id in USERS:
            print(f"Ошибка: пользователь с ID {user_id} уже существует.")
        else:
            try:
                # Пробуем создать нового пользователя (внутри конструктора User есть проверка email)
                user = User(username=username, email=email, user_id=user_id)

                # Добавляем пользователя в словарь USERS
                USERS[user_id] = user

                # Уведомляем об успешном создании
                print(f"✅ Пользователь создан: {user}")

            except ValueError as e:
                # Если возникла ошибка (например, некорректный email) — выводим её
                print(f"Ошибка при создании пользователя: {e}")

    elif args.command == "create-account":
        balance = args.balance  # сохраняем балланс из аргументов
        user_id = args.user_id  # Сохраняем ID пользователя из аргументов

        # Проверяем, существует ли уже пользователь с таким ID
        if user_id not in USERS:
            print(f"Ошибка: пользователь с ID {user_id} не существует.")
        else:  # создаем счет для пользователя
            user = USERS[user_id]  # получаем объект пользователя
            balance = float(balance)
            account = BankAccount(user=user, balance=balance)  # создаем аккаунт
            user.add_account(account)  # добавляем счет пользователю
            ACCOUNTS[user_id] = account  # сохраняем в глобалный
            print("Счёт успешно создан!")
            print(account)  # используем __str__, он у нас реализован
    elif args.command == "deposit":
        user_id = args.user_id  # Получаем ID пользователя из аргументов
        amount = float(args.amount)  # Сумму приводим к типу float

        # Проверяем, существует ли пользователь
        if user_id not in USERS:
            print(f"❌ Пользователя с ID {user_id} не существует.")

        # Проверяем, существует ли счёт у пользователя
        elif user_id not in ACCOUNTS:
            print(f"❌ У пользователя {user_id} нет открытых счетов.")

        else:
            user = USERS[user_id]  # Получаем объект пользователя
            account = ACCOUNTS[user_id]  # Получаем его счёт

            # Выполняем пополнение баланса
            account.deposit(amount)

            # Создаём объект транзакции
            transaction = Transaction(
                type="deposit",  # Тип операции
                amount=amount,  # Сумма
                sender=None,  # Отправителя нет (банковское пополнение)
                receiver=user,  # Получатель — пользователь
            )

            # Если у пользователя ещё нет журнала операций — создаём его
            if user_id not in LOGS:
                LOGS[user_id] = TransactionLog()

                # Добавляем транзакцию в журнал
            LOGS[user_id].add(transaction)

            # Подтверждаем выполнение
            print(f"✅ Счёт пополнен. Новый баланс: {account.balance}")

    elif args.command == "withdraw":
        user_id = args.user_id  # Получаем ID пользователя из аргументов
        amount = float(args.amount)  # Сумму приводим к типу float

        # Проверяем, существует ли пользователь
        if user_id not in USERS:
            print(f"❌ Пользователя с ID {user_id} не существует.")

        # Проверяем, существует ли счёт у пользователя
        elif user_id not in ACCOUNTS:
            print(f"❌ У пользователя {user_id} нет открытых счетов.")

        # Проверяем, что сумма положительная
        elif amount <= 0:
            print("❌ Сумма должна быть больше нуля.")

        # Проверяем, что на счету достаточно средств
        elif ACCOUNTS[user_id].balance < amount:
            print("❌ Недостаточно средств на счёте.")

        else:
            user = USERS[user_id]  # Получаем объект пользователя
            account = ACCOUNTS[user_id]  # Получаем его счёт

            # снимаем денежные средства
            account.withdraw(amount)

            # Создаём объект транзакции
            transaction = Transaction(
                type="withdraw",  # Тип операции
                amount=amount,  # Сумма
                sender=user,  # Отправителя нет (банковское пополнение)
                receiver=None,  # Получатель — банк
            )
            # Если у пользователя ещё нет журнала операций — создаём его
            if user_id not in LOGS:
                LOGS[user_id] = TransactionLog()

            # Добавляем транзакцию в журнал
            LOGS[user_id].add(transaction)
            print(f"✅ Денежные средства сняты. Новый баланс: {account.balance}")

    elif args.command == "transfer":
        from_user_id = args.from_user_id
        to_user_id = args.to_user_id
        amount = float(args.amount)

        # Блок проверок
        if from_user_id not in USERS:
            print("❌ Отправитель не найден")
        elif to_user_id not in USERS:
            print("❌ Получатель не найден")
        elif from_user_id not in ACCOUNTS:
            print("❌ У отправителя нет счёта")
        elif to_user_id not in ACCOUNTS:
            print("❌ У получателя нет счёта")
        elif amount <= 0:
            print("❌ Сумма должна быть больше нуля.")
        elif ACCOUNTS[from_user_id].balance < amount:
            print("❌ Недостаточно средств на счёте.")
        # осной код блока
        else:
            user_sender = USERS[
                from_user_id
            ]  # Получаем объект пользователя отправителя
            account_sender = ACCOUNTS[from_user_id]  # Получаем его счёт
            user_reciver = USERS[to_user_id]  # Получаем объект пользователя
            account_reciver = ACCOUNTS[to_user_id]  # Получаем его счёт

            account_sender.transfer(amount, user_reciver)  # Проводин транзакцию

            # Создаём объект транзакции
            transaction = Transaction(
                type="transfer",  # Тип операции
                amount=amount,  # Сумма
                sender=user_sender,  # Отправитель
                receiver=user_reciver,  # Получатель
            )

            if from_user_id not in LOGS:
                LOGS[from_user_id] = TransactionLog()

            # Добавляем транзакцию в журнал
            LOGS[from_user_id].add(transaction)
            print(f"✅ Денежные средства сняты. Новый баланс: {account_sender.balance}")

            if to_user_id not in LOGS:
                LOGS[to_user_id] = TransactionLog()

            # Добавляем транзакцию в журнал
            LOGS[to_user_id].add(transaction)

    elif args.command == "show-log":
        user_id = args.user_id  # Получаем ID пользователя из аргументов

        # Проверяем, существует ли пользователь с таким ID
        if user_id not in USERS:
            print(f"❌ Пользователь с ID {user_id} не найден.")

        # Проверяем, есть ли у пользователя журнал операций
        elif user_id not in LOGS:
            print(f"ℹ️ У пользователя с ID {user_id} ещё нет операций.")

        else:
            # Выводим заголовок с именем пользователя
            print(f"📘 История операций пользователя {USERS[user_id].username}:")

            # Проходимся по всем операциям в журнале и выводим их
            for txn in LOGS[user_id]:
                print(txn)  # Вывод строки транзакции (__str__ в классе Transaction)

    elif args.command == "filter-type":
        user_id = args.user_id  # Получаем ID пользователя из аргументов
        type = (
            args.type
        )  # Получаем тип транзакции из аргументов (уже проверен через choices)

        # Проверка существования пользователя
        if user_id not in USERS:
            print(f"❌ Пользователь с ID {user_id} не найден.")

        # Проверка наличия журнала операций
        elif user_id not in LOGS:
            print(f"ℹ️ У пользователя с ID {user_id} ещё нет операций.")

        else:
            # Заголовок
            print(f"📘 История операций пользователя {USERS[user_id].username}:")
            found = False  # Флаг для отслеживания, найдены ли подходящие транзакции

            # Перебор всех транзакций пользователя
            for txn in LOGS[user_id]:
                if txn.type == type:  # Сравниваем тип транзакции
                    print(txn)
                    found = True  # Отмечаем, что найдено совпадение

            # Если ни одна транзакция не подошла — сообщаем
            if not found:
                print("⚠️ Операции с таким типом не найдены.")

    elif args.command == "filter-date":
        user_id = args.user_id  # Получаем ID пользователя из аргументов
        date = args.date  # Получаем дату из аргументов (в формате дд.мм.гггг)

        # Проверка: существует ли пользователь
        if user_id not in USERS:
            print(f"❌ Пользователь с ID {user_id} не найден.")

        # Проверка: есть ли у него лог операций
        elif user_id not in LOGS:
            print(f"ℹ️ У пользователя с ID {user_id} ещё нет операций.")

        else:
            print(f"📘 Операции пользователя {USERS[user_id].username} за {date}:")
            results = LOGS[user_id].filter_by_date(
                date
            )  # Получаем список транзакций за дату

            if results:
                for txn in results:
                    print(txn)
            else:
                print("Нет операций за эту дату.")

    else:
        parser.print_help()


def show_balance(users, accounts, logs, args):
    if args.account_id not in accounts:
        print("❌ Счёт не найден.")
        return

    acc = accounts[args.account_id]
    print(f"💳 Баланс счёта {acc.account_id}: {acc.balance}₽")


def show_log(users, accounts, logs, args):
    if args.account_id not in logs:
        print("❌ Журнал для счёта не найден.")
        return

    log = logs[args.account_id]
    if not log.transactions:
        print("📭 Журнал пуст.")
        return

    print(f"📜 Журнал операций по счёту {args.account_id}:")
    for tx in log.transactions:
        print(tx)


def filter_type(users, accounts, logs, args):
    if args.account_id not in logs:
        print("❌ Журнал для счёта не найден.")
        return

    log = logs[args.account_id]
    filtered = log.filter_by_type(args.tx_type)
    if not filtered:
        print("📭 Нет транзакций такого типа.")
        return

    print(f"📘 Фильтр по типу '{args.tx_type}':")
    for tx in filtered:
        print(tx)


def filter_date(users, accounts, logs, args):
    if args.account_id not in logs:
        print("❌ Журнал для счёта не найден.")
        return

    log = logs[args.account_id]
    filtered = log.filter_by_date(args.date)
    if not filtered:
        print(f"📭 Нет транзакций за {args.date}.")
        return

    print(f"🗓️ Фильтр по дате {args.date}:")
    for tx in filtered:
        print(tx)


if __name__ == "__main__":
    main()
