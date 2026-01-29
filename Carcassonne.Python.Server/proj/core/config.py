import os
from dotenv import load_dotenv, dotenv_values

__config = {
    **dotenv_values(".env"),
    **os.environ
}

def __getBooleanValue(key: str, default: bool = False) -> bool:    
    value = __config.get(key, default).lower()
    return value == "true" or value == "1" or value == "yes"

def __getIntegerValue(key: str, default: int = 0) -> int:
    try:
        return int(__config.get(key, default))
    except ValueError:
        return default

appName: str = __config.get("appName")
debug: bool = __getBooleanValue("debug")
port: int = __getIntegerValue("port", 8000)
host: str = __config.get("host", "127.0.0.1")

connectionString: str = __config.get("connectionString")

print(appName, debug, port, host)
