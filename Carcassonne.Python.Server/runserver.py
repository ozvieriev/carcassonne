from os import environ
import uvicorn

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '127.0.0.1')
    try:
        PORT = int(environ.get('SERVER_PORT', '8000'))
    except ValueError:
        PORT = 8000

    uvicorn.run("proj:app", host=HOST, port=PORT, reload=True, log_level="debug")
