import os

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
from google.auth.transport import requests
from google.oauth2 import id_token


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
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.environ["GAUTH_CLIENT_ID"])

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        if idinfo['hd'] != "iiitd.ac.in":
            raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        return idinfo['email']
    except ValueError:
        # Invalid token
        return ""


def main():
    aes_key = "1767d6c93ef346425abb20187143e0bca07ef895c49458f4851611a920a1f16ccdb791d79828464edaeb371c8031a52cbefd336d1666dfb3807cd53ddf26fb263a65ebf1b71d7178a6a11dfb884fc7c116c24fe234aaf8a747b1c592ebbe3b169aa74b67503169a7718f5c450b585470018d0dc9655cb41a0c76adc45dabe19700ffeb645c78aa62b244c1bd5bdd0401d6210a3d62fcdbf7e363ebed66b4c6161eccf7ae57458b9b157e9e5e066e8d114a5fb48e7827c05d0ee43d0a58eb89e109a06d04b96b0e498f08bc743544ba85db6ab1be6ce089f3bcfd31e726b4804c57b941791982b3badf93444c5450a381772d04bc223bdc04bb9fc876924b3978f8956752223a122b0a0a9079282850b012938586ef3792e0f938381c4b9fa3367568f41b1912ef12f830c131b23c06cb9811259a0a9114cd9b8e0d8c1ed18a501b2eeb09d6b9c17ab6db7582949a0ee2be132771165c2148406ff81400fbcb8816c5a911532f0fce22021a37b6aa7699dda0757a690636e277117752f8ee969cbe3e008edfb52ca92c0b24cde260bfe059a4d14bc05b830f7c320bb892d0e2fa13d046b08b19811d681a2f3adae77ea934fb73f60d0a5ff9a63c70adf9d998ae349d43dc86e95119207abf8483c6ffe35e056c9f61960337e939c3cf2189ab2b1e1b1f7a2adf0f6e424807e27642abbba5a80eababa48c5d57a5aa3ebf7a729a"
    token = "536693223e7e983f46d000ce458a0db6a09db7fdcbcff7b392bb03b28f87312d3288f13ca0949b37852cb81b762dcedde9f63cde181375cbdfa299d7899046d52d2f19e809844d0a400a757387c67f58dd14bcf8ade8184c8a91d5dc8a9484722d298f60e32509216172ed9d269a760def6ac3b567f387da366e92a5660f3a5b09b709fcf8a8387e52e3e5248d025d1124d5f4586e0161df836b93f0a444a52f9a76b947da1a4c9acfdb4200bce33957a766714a6e76322645e0461ba696507ae707565ab41279f409f90925c70b862719741f978d0cbc48fb8587d91688640790b08370dae7720c48f898198abd4f68dbc28fbf3b14031013d6579e6ef75c200824138ae3969e5f33b9590b6a1f9e288f0350e21f66a06a09133f7927889127fc549ec12166e30de3d30ded35ccfcf4b68409bdc7d63741b7f922afc6fc026a820cb03a3ba86b8d992b7b94f5a267e7366c22331f2038ee42f4906140fec969566291b8f73170a72023ca372e8926e5a201b36d756d12e55efa65431285579b61cf9d59268249a987a592bab05993987efcbc192e4eccdb8bff3635821d12bef958c44045b55f7925cc27db7ed6c4d5ce4f95f16d23ceb5bee7b33c120ec85d4b14f6839f718fadf177f2f74021b576b80eee3801221224bb74a5a3ba5221e49fc71ab1ecc34119401a9ed23d327932ea3f818051ba33116f3cb40d4c90bbee0cd2ce141e0cb3485a7d822082f0d762117848f4e63078815e91e17f25340bd4b0c73c648196fbd0422e6875a1b7a31442ae25ed39f50018881a8e91e4a08a6b2a2719963608534ceabb0d8898d54240e0d526627290d99674284ee4f87628bee4af5ec5fc5383cddb93f027e321f099d833106d6ebdd7007db4fffd7bc2deab10039faa262afc55022f762a24a92f960631c471a24fcfd84b4028430618cddca73a941f64bfb092e4c9472ffc16f3e3c99b11aefb64047507cd5e2b1da48ed10c050c2bd92b9a0e37f6d8ddc988101e96d969087e9e5ff53fad76b1957df36ba87bebe6386c247df74974df56d1abea5c94b79b2d672ffca3aac9dcbe01996a8c1454d93c4f07035438576ebd914722006d0d85d0135c0a77a28250ee64eca192bbc6822c69b911a010e4b68ca315a035361f4fe32f6996d627e989e89e05a679e5b941f6750ee5cace74891b3657135b666034a9eadc604c8e0d1545a67328cf56fc317e683db116c02c406a792691d8878cb6d622d41528fdc6e93b01eb8dd5fdee3ce0d27134721ae4fd61c8c3107191249aa2ef41ace61b5573e08528f7d4cdc7fb9cc6b1e4b99adc19230c307101543327f40b4073d7908728f112dd465a5d9bca44b11fd50275ae3707f978f507468853a99cf0609a4de1abe94740529f77e8c2fe1b743542596c87af0592d15a65c1e1b3658354f65e5a4a969ba4851e582815194de3c1eb9adb2c86557f2731717e961c69393d5d2a805866439983859e73154587176ae42db8693fb155adf76bda209c0a54535fd16e0041a1e88280c2f53fcead9b85338d67b70c09081eb623ca93e689b05e2674be9632e141fa07f8541ab69ba4add78ce53061af0db393de13d7c70c84a4fab20838ce16fce6e9f96d170986e5cc3016effbcd1751af7e2e23ff19f5c221707a0c30076351998c0b9c305c2913c42930e40cccd85c511d4095d551f3dfdb80fec392768744947060575538e1abaf500a4bc95622bb3652c0c860f29367bd40ca06f222bb218f301617d07c067431e7dff79b19d5934a"
    iv = "c8a7775ef7a069494936040afc627d8d"
    print(len(aes_key) + len(token) + len(iv))
    print(authenticate(token, aes_key, iv))


if __name__ == "__main__":
    main()
