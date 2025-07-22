import json
import jwt
from jwcrypto import jwk
from src.infra.authenticator.authenticator import IAuthenticator

class JWTDriver(IAuthenticator):
    def __init__(self, private_jwk_json_str: str, public_jwk_json_str: str):
      private_jwk_dict = json.loads(private_jwk_json_str)
      public_jwk_dict = json.loads(public_jwk_json_str)

      private_key_obj = jwk.JWK(**private_jwk_dict)
      public_key_obj = jwk.JWK(**public_jwk_dict)

      self._private_key = private_key_obj.export_to_pem(private_key=True, password=None)
      self._public_key = public_key_obj.export_to_pem()

    def generate_token(self, payload):
      return jwt.encode(payload, self._private_key, algorithm="RS256")

    def decode_token(self, token):
      try:
        return jwt.decode(token, self._public_key, algorithms=["RS256"])
      except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
      except jwt.InvalidTokenError:
        raise ValueError("Token invalid")