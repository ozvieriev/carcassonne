from pydantic import BaseModel
from .pointApiModel import *

class gamePlaceTileRequest(BaseModel):
    location: pointApiModel
    rotation: int
