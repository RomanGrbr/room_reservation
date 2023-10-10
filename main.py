# import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.api.meeting_room import router


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url='/swagger',
    redoc_url='/redoc'
    )

app.include_router(router)

# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)
