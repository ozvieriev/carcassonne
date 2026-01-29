import uvicorn
from os import environ
from proj.core import config
from proj.game.models import *

if __name__ == '__main__':
    uvicorn.run("proj:app", host=config.host, port=config.port,
                reload=config.debug, log_level="debug")
