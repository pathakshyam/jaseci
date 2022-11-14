from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from allauth.socialaccount.providers.okta.views import OktaOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from jaseci_serv.jsx_oauth import serializers
from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from jaseci_serv.jsx_oauth.models import SocialLoginProvider, PROVIDERS_MAPPING
from allauth.socialaccount.models import SocialApp
from jaseci_serv.jsx_oauth.utils import JSXSocialLoginView

# from jaseci_serv.jsx_oauth.permissions import IsValidateLicense


class ExampleUrlView(GenericAPIView):
    serializer_class = serializers.GetExampleUrlSerializer
    # permission_classes = [IsValidateLicense]

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        provider = serializer_data.validated_data.get("provider")
        callback_url = f"{request.build_absolute_uri('/')[:-1]}{settings.DEFAULT_CALLBACK_URL_FOR_SSO}"
        social_app = SocialApp.objects.filter(provider=provider.lower()).first()
        if social_app:
            return Response(
                {
                    "url": PROVIDERS_MAPPING[provider]["LOGIN_URL"].format(
                        callback_url=callback_url, client_id=social_app.client_id
                    )
                }
            )
        else:
            return Response(
                {
                    "error": f"Social login applications for the {provider} not configured properly"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class GoogleLogin(JSXSocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    provider = SocialLoginProvider.GOOGLE
    client_class = OAuth2Client


class FaceBookLogin(JSXSocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    provider = SocialLoginProvider.FACEBOOK
    client_class = OAuth2Client


class GitHubLogin(JSXSocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    provider = SocialLoginProvider.GITHUB
    client_class = OAuth2Client


class OktaLogin(JSXSocialLoginView):
    adapter_class = OktaOAuth2Adapter
    provider = SocialLoginProvider.OKTA
    client_class = OAuth2Client


class MicrosoftLogin(JSXSocialLoginView):
    adapter_class = MicrosoftGraphOAuth2Adapter
    provider = SocialLoginProvider.MICROSOFT
    client_class = OAuth2Client


class OpenIdLogin(JSXSocialLoginView):
    adapter_class = GitHubOAuth2Adapter  # TODO: create custom adaptor for OpenID
    provider = SocialLoginProvider.OPENID
    client_class = OAuth2Client


class GoogleExampleLiveView(View):
    template_name = "examples/google_sso.html"

    def get(self, request):
        code = request.GET.get("code")
        social_app = SocialApp.objects.filter(
            provider=SocialLoginProvider.GOOGLE.lower()
        ).first()
        redirect_uri = f"{request.build_absolute_uri('/')[:-1]}{settings.DEFAULT_CALLBACK_URL_FOR_SSO}"
        return render(
            request,
            self.template_name,
            {
                "code": code,
                "client_id": social_app.client_id,
                "callback_url": redirect_uri,
            },
        )
