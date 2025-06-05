from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    inject_container = None

    def ready(self):
        from users.inject import UsersContainer
        import users

        self.inject_container = UsersContainer()
        self.inject_container.wire(
            packages=[users],
            modules=[],
        )
