import os

from google.auth.transport import requests
from google.oauth2 import id_token
from firebase_admin import auth


def verify_token(token: str) -> tuple:
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ["GAUTH_CLIENT_ID"])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != "iiitd.ac.in":
        #     raise ValueError('Wrong hosted domain.')

        # Get the user's Google Account ID from the decoded token.
        return idinfo['email'], idinfo['picture']
    except ValueError:
        # Invalid token
        return "", None


def create_firebase_token(user) -> str:
    uid = str(user.pk)
    managed_clubs = list(user.club_coordinator_of.values_list("username", flat=True))
    additional_claims = {
        "clubs": managed_clubs
    }
    custom_token = auth.create_custom_token(uid, additional_claims)
    return custom_token.decode("utf-8")
