from django.apps import AppConfig


class AppsConfig(AppConfig):
    """
        Класс конфигурации приложения Django.

        :param default_auto_field: Поле, используемое для автоматического создания первичных ключей.
        :type default_auto_field: str
        :param name: Имя приложения.
        :type name: str
        :param label: Ярлык приложения.
        :type label: str
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps'
    label = 'apps'
