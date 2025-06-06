from dependency_injector import containers, providers

from users.services import GoogleRawLoginUseCase

class UsersContainer(containers.DeclarativeContainer):
    google_raw_login_use_case = providers.Factory(GoogleRawLoginUseCase)
