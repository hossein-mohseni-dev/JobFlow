from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)
        raw = request.COOKIES.get("jobflow_access")
        if not raw:
            return None
        try:
            validated = self.get_validated_token(raw)
        except InvalidToken:
            return None
        return self.get_user(validated), validated
