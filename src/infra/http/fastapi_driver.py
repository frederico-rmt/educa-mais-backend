import traceback
from fastapi import FastAPI, HTTPException, Request
from typing import Callable
from src.infra.authenticator.authenticator import IAuthenticator

class FastAPIAdapter:
  def __init__(self, authenticator: IAuthenticator):
    self.app = FastAPI()
    self.authenticator = authenticator

  def register(self, method: str, path: str, callback: Callable, is_private: bool = True):
    async def endpoint(request: Request):
      try:
        headers = dict(request.headers)
        query = dict(request.query_params)
        params = dict(request.path_params)
        body = await request.json() if method.lower() in ['post', 'put', 'patch'] else {}
        if is_private:
          auth_header = headers.get("authorization")
          if not auth_header or not auth_header.lower().startswith("bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
          token = auth_header.split(" ")[1]
          try:
            decoded = self.authenticator.decode_token(token)
            request.state.user = decoded
          except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        response = await callback(headers, query, params, body)
        return response

      except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
      except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    getattr(self.app, method.lower())(path)(endpoint)