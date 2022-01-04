from fastapi import FastAPI
import uvicorn
from api import motd, pets
from views import home
from starlette.staticfiles import StaticFiles
from environs import Env


main_app = FastAPI()


def configure():
    configure_routing()
    configure_env_vars()


def configure_env_vars():                                             
    env = Env()                                                       
    env.read_env()                                                    
    if not env("ENV_STRING"):                                         
        print(f"WARNING: environment variable ENV_STRING not found") 
        raise Exception("environment variable ENV_STRING not found.") 
    else:                                                             
        home.env_string = env("ENV_STRING")                           


def configure_routing():
    main_app.mount('/static', StaticFiles(directory='static'), name='static')
    main_app.include_router(motd.router)
    main_app.include_router(pets.router)
    main_app.include_router(home.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(main_app, host='0.0.0.0', port=8000)
else:
    configure()
