import uvicorn
from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url='/swagger',
    redoc_url='/redoc'
    )


# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)