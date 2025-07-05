class User:

    def __init__(self, username, email, user_id):
        self.username = username
        if not self.is_valid_email(email):
            raise ValueError("Некорректный email")
        self.email = email
        self.user_id = user_id

    def is_valid_email(self, email):
        return "@" in email and "." in email.split("@")[-1]

    def update_email(self, new_email):
        if not self.is_valid_email(new_email):
            raise ValueError("Некорректный email")
        self.email = new_email

    def __str__(self):
        return (
            f"У пользователя {self.username} с id: {self.user_id} email: {self.email}"
        )
