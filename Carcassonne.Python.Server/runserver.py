import uvicorn
from os import environ
from proj.api.settings import config
from proj.core.models import *

if __name__ == '__main__':
    uvicorn.run("proj.api:app", host=config.host, port=config.port,
                reload=config.debug, log_level="debug")
