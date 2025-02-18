# -*- encoding: utf-8 -*-


from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
    Класс AuthConfig наследуется от AppConfig из фреймворка Django и используется для конфигурации приложения apps.auth.

    Этот класс используется для определения конфигурации приложения, которое может быть подключено в проект Django,
    и чтобы указать, как именно приложение будет настроено и функционировать в контексте проекта.

    Параметры:
    ----------
    AppConfig : class
        используется в Django для конфигурирования приложений

    Атрибуты:
    ----------
    name : str
        Полное имя пакета приложения.
    label : str
        Метка приложения, используемая в URL-адресах и некоторых других местах.
    """
    name = 'apps.auth'
    label = 'apps_auth'
    
