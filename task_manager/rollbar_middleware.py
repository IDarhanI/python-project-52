from rollbar.contrib.django.middleware import RollbarNotifierMiddleware


class CustomRollbarNotifierMiddleware(RollbarNotifierMiddleware):
    def get_extra_data(self, request, exc):
        """
        Add custom data to Rollbar payload.
        """
        extra_data = dict()

        # Пример добавления произвольных метаданных (опционально)
        extra_data = {
            "trace_id": "aabbccddeeff",
            "feature_flags": [
                "feature_1",
                "feature_2",
            ],
        }

        return extra_data

    def get_payload_data(self, request, exc):
        """
        Add user information to Rollbar payload.
        """
        payload_data = dict()

        if not request.user.is_anonymous:
            # Добавляем информацию о пользователе, затронутом этим событием
            # Поле 'id' обязательно, все остальное опционально
            payload_data = {
                "person": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email
                    if hasattr(request.user, "email")
                    else None,
                },
            }

        return payload_data
