import os
import requests
from django.contrib.auth.models import User
from requests_oauthlib import OAuth2Session
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.http import JsonResponse

# OAuth Configuration ENV variables -> To move to .env file
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

# OAuth endpoints given in the GitHub API documentation
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

GITHUB_API_URL = "https://api.github.com/user"

@api_view(["GET"])
def login_github(request):
    """Returns the GitHub authorization URL."""
    github = OAuth2Session(GITHUB_CLIENT_ID)
    auth_url, _ = github.authorization_url(GITHUB_AUTH_URL)
    return JsonResponse({"auth_url": auth_url})

@api_view(["GET"])
def github_callback(request):
    """Handles GitHub OAuth callback and returns an authentication token."""
    
    github = OAuth2Session(GITHUB_CLIENT_ID)
    code = request.GET.get("code")
    token = github.fetch_token(GITHUB_TOKEN_URL, client_secret=GITHUB_CLIENT_SECRET, code=code)

    headers = {"Authorization": f"Bearer {token['access_token']}"}
    user_data = requests.get(GITHUB_API_URL, headers=headers).json()
    
    user, _ = User.objects.get_or_create(username=user_data["login"])    
    profile, _ = UserProfile.objects.get_or_create(
        user=user, 
        defaults={
            "github_id": user_data["id"],
            "username": user_data["login"],
            "avatar_url": user_data["avatar_url"]
        }
    )

    refresh = RefreshToken.for_user(user)
    refresh["username"] = user.username

    return JsonResponse({
        'refresh': str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "username": user.username,
            "avatar_url": profile.avatar_url
        }
    })
