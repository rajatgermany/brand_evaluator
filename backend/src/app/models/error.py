from pydantic import BaseModel


class Error(BaseModel):
    status_code: str
    msg: str
