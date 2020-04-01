from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialConnectView
from rest_auth.social_serializers import TwitterConnectSerializer

class FacebookConnectView(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter

class TwitterConnectView(SocialConnectView):
    serializer_class = TwitterConnectSerializer
    adapter_class = TwitterOAuthAdapter

class GithubConnectView(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = '/'
    client_class = OAuth2Client





