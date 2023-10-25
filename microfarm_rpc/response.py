import typing as t
from pydantic import BaseModel


R = t.TypeVar('R')


class RPCResponse(BaseModel, t.Generic[R]):
    code: int
    type: str
    body: R | None = None
    description: str | None = None
