from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# аутентификационный роутер (Auth router) — предоставляет доступ к эндпоинтам
# /login (для аутентификации) и /logout (для завершения сессии)
router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

# регистрационный роутер (Register router) —  предоставляет доступ к эндпоинту
# /register для регистрации нового пользователя
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

# роутер пользователей (Users router) — предоставляет доступ к эндпоинтам
# управления пользователями (чтение из БД, удаление, обновление)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)
