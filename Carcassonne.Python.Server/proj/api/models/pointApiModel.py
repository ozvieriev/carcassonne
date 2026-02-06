from pydantic import BaseModel


class pointApiModel(BaseModel):
    x: int
    y: int
