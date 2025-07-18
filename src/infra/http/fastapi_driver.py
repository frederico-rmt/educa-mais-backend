import traceback
from fastapi import FastAPI, HTTPException, Request
from typing import Callable

class FastAPIAdapter:
  def __init__(self):
    self.app = FastAPI()

  def register(self, method: str, path: str, callback: Callable):
    async def endpoint(request: Request):
      try:
        headers = dict(request.headers)
        query = dict(request.query_params)
        params = dict(request.path_params)
        body = await request.json() if method.lower() in ['post', 'put', 'patch'] else {}

        response = await callback(headers, query, params, body)
        return response

      except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
      except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    getattr(self.app, method.lower())(path)(endpoint)