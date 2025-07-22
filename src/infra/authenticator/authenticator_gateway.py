from src.infra.authenticator.authenticator import IAuthenticator

class AuthenticatorGateway(IAuthenticator):
  def __init__(self, authenticator_driver: IAuthenticator):
    self._authenticator_driver = authenticator_driver

  def decode_token(self, token):
    return self._authenticator_driver.decode_token(token)

  def generate_token(self, payload):
    return self._authenticator_driver.generate_token(payload)