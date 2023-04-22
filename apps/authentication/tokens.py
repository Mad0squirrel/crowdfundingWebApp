import six as six
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# from django.utils import six
class TokenGenerator(PasswordResetTokenGenerator):
    """
        Генератор токена для сброса пароля.

        Методы:
        --------
        _make_hash_value(self, user, timestamp):
            Создает хеш для токена.
        """

    def _make_hash_value(self, user, timestamp):
        """
        Создает хеш для токена на основе id пользователя, временной метки и его пароля.

        Параметры:
        ----------
        user: User
            Объект пользователя.
        timestamp: datetime
            Временная метка.

        :return: str: Хеш для токена.
        """
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + user.password +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
