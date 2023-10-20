# import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_first_superuser


app = FastAPI(
    title=settings.app_title,
    description=settings.description,
    docs_url='/swagger',
    redoc_url='/redoc'
    )

# Подключаем роутер.
app.include_router(main_router)


# При старте приложения запускаем корутину create_first_superuser.
@app.on_event('startup')
async def startup():
    await create_first_superuser()

# Для выполнения действий в момент остановки приложения
# @app.on_event('shutdown')


# if __name__ == '__main__':
#     uvicorn.run('main:app', reload=True)
