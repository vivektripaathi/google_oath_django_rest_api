from dependency_injector import containers, providers

from users.domain.use_cases.google_raw_login_use_case import GoogleRawLoginUseCase

class UsersContainer(containers.DeclarativeContainer):
    google_raw_login_use_case = providers.Factory(GoogleRawLoginUseCase)
