import os
from dotenv import load_dotenv

load_dotenv()

AUTHORIZATION_BASE_URL = "https://login.microsoftonline.com"
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORITY = f"{AUTHORIZATION_BASE_URL}/{os.getenv('TENANT_ID')}"

REDIRECT_PATH = "/callback"

SCOPE = ["email", "User.Read", "Mail.Read", "Mail.Send"]

API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/messages"
API_ENDPOINT_USER = "https://graph.microsoft.com/v1.0/me"

SESSION_TYPE = "filesystem"

# OAuth2 endpoints
AUTHORIZE_URL = f"{AUTHORIZATION_BASE_URL}/{os.getenv('TENANT_ID')}/oauth2/v2.0/authorize"
TOKEN_URL = f"{AUTHORIZATION_BASE_URL}/{os.getenv('TENANT_ID')}/oauth2/v2.0/token"
DEVICE_URL = f"{AUTHORIZATION_BASE_URL}/{os.getenv('TENANT_ID')}/oauth2/v2.0/devicecode"