# bank/cli.py

import argparse

from bank.user import User
from bank.utils.account import BankAccount
from bank.utils.transaction import Transaction, TransactionLog

USERS = {}
ACCOUNTS = {}


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
        "--from-user-id", required=True, type=int, help="ID отправителя"
    )
    group_transfer.add_argument(
        "--to-user-id", required=True, type=int, help="ID получателя"
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

    # filter-type
    filter_type = subparsers.add_parser(
        "filter-type", help="Фильтровать операции по типу."
    )
    group_ftype = filter_type.add_argument_group("фильтр по типу")
    group_ftype.add_argument(
        "--user-id", required=True, type=int, help="ID пользователя"
    )
    group_ftype.add_argument(
        "--type",
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
        ...
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
