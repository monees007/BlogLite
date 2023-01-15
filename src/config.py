import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID",
                                  '846448875684-5kca9r1coj09ha193jhist3j66m7mcvs.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "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")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
