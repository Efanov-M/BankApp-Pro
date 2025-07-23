#!/usr/bin/env python3
# Файл main.py — точка входа для всей программы


# from bank.utils import file_manager
from bank.utils.cli import main as cli_main
from bank.utils.file_manager import load_accounts, load_logs, load_users

# from bank.utils.account import BankAccount
# from bank.utils.transaction import Transaction, TransactionLog


# Загружаем все данные
USERS = load_users()
ACCOUNTS = load_accounts()
LOGS = load_logs()

if __name__ == "__main__":
    cli_main()
