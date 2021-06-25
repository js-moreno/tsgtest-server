from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    def get_additional_claims(self, request):
        return {
            "first_name": request.user.first_name,
            "is_staff": request.user.is_staff,
        }
