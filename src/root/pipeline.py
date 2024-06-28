from typing import Any, Dict

from users.serializers import UserSerializer


def save_user_details(
    backend: Any,
    user: Any,
    response: Dict[str, Any],
    *args: Any,
    **kwargs: Any
) -> None:
    if backend.name == 'google-oauth2':
        user_data: Dict[str, Any] = {
            'username': user.username,
            'avatar': response.get('picture') if not user.avatar else user.avatar,
        }

        serializer: UserSerializer = UserSerializer(user, data=user_data, partial=True)

        if serializer.is_valid():
            serializer.save()
