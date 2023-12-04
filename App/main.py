from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from App.core.config import settings
from App.routes import router as main_route



def get_application() -> FastAPI:
    ''' Configure, start and return the application '''

    ## Start FastApi App
    application = FastAPI(
        title="X Server",
        summary="x API",
        version="0.0.1",
        contact={
            "name": "Usman Fawad",
            "email": "ufawad0@gmail.com",
        },
    )

    application.include_router(main_route)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application



app = get_application()

