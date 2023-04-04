import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID",
                                  'temp-secret-removed')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "temp-secret-removed")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
