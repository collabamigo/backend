import os

from Cryptodome.Cipher import PKCS1_OAEP, AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Util.Padding import unpad
from google.auth.transport import requests
from google.oauth2 import id_token


# TODO: See if pyca/cryptography can be used

def authenticate(encrypted_token: str, aes_key: str, iv: str) -> str:
    """

        :parameter iv: Initialization Vector for AES
        :parameter aes_key: AES key encrypted with RSA
        :parameter encrypted_token: Token encrypted with aes_key
        :return: User's email if authenticated, blank if not
    """
    token = _aes_decrypt(encrypted_token, _rsa_decrypt(aes_key), iv)
    print(len(token))
    return _verify_token(token)


def _rsa_decrypt(ciphertext: str) -> str:
    ciphertext = bytes.fromhex(ciphertext)
    private_key = RSA.importKey(os.environ['TOKEN_PVT_KEY'])
    private_key_object = PKCS1_OAEP.new(private_key)
    plaintext = private_key_object.decrypt(ciphertext)
    return plaintext.decode()


def _aes_decrypt(ciphertext: str, aes_key: str, iv: str) -> str:
    iv = bytes.fromhex(iv)
    aes_key = bytes.fromhex(aes_key)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))
    return unpad(plaintext, 16).decode()


def _verify_token(token: str) -> str:
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ["GAUTH_CLIENT_ID"])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        if idinfo['hd'] != "iiitd.ac.in":
            raise ValueError('Wrong hosted domain.')

        # Get the user's Google Account ID from the decoded token.
        return idinfo['email']
    except ValueError:
        # Invalid token
        return ""


def main():
    aes_key = ""
    t = ""
    iv = ""
    print(len(aes_key) + len(t) + len(iv))
    print(authenticate(t, aes_key, iv))


if __name__ == "__main__":
    main()
