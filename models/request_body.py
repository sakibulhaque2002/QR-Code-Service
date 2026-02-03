#request_body.py

from pydantic import BaseModel

class RequestBody(BaseModel):
    jwt: str
    payload: str