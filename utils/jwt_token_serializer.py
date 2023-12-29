from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JWTTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        scope_names_string = ' '.join(user.scopes.values_list('name', flat=True))
        token['scopes'] = scope_names_string
        return token
